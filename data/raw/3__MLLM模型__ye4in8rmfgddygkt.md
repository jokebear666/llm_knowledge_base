# 3️⃣ MLLM模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/ye4in8rmfgddygkt -->

# 优化
## MLLM输出框坐标的两个优化方案
以吐token的形式输出坐标

【方案1】 前向的时候做采样，得到-一个pred结果。定位到pred中输出坐标值的那些token， 将这些token的交叉熵loss严格改为回归大小。改法如下：计算当前token采样到的pred坐标值与label坐标值回归大小的标量权重W，将该token原本的交叉熵loss除以该交叉熵loss的标量值，再乘上W，严格转化为回归大小oss，

【方案2】做online的数据增强，给label中的每个坐标值做一个比较小的正态分布千扰，保证词表中的许多靠近真值的坐标值都能被计算交叉熵。越靠近坐标真值的数值，计算交叉熵的次数越多，概率提升的次数也越多

个人觉得两个方案都有缺陷。方案1看似让loss大小与坐标值预测误差保持一致，实际上还是个分类问题方案1只会让正确坐标值的输出概率基于采样误差来控制更新幅度，对于其他与真值相近的坐标值的采样概率没有精准控制，没有解决分类模型做回归任务的根本问题，方案2，越与真值靠近的坐标值越有可能更新概率，如果同源样本的online增强采样足够多，最终训出来的模型，更靠近真值的坐标值，输出的概率就会更大，这好像就变成一个类似回归的问题了。但是可能需要很小的学习率来训很多的epoch，才能既保证不过拟合叉保证同源样本的online增强采样足够多。





## 动态分辨率（不同分辨率图像如何处理）<font style="color:#D22D8D;">(by草莓师姐)</font>
:::color3
**简介：**<font style="color:rgb(51, 51, 51);">Qwen2-VL 可以</font>**<font style="color:#74B602;">处理任意图像分辨率</font>**<font style="color:rgb(51, 51, 51);">，将其映射为动态数量的视token，提供更接近人类的视觉处理体验。</font><font style="color:rgb(25, 27, 31);">不再将</font>**<font style="color:#ED740C;">图像统一Resize到VIT的接收尺寸再输入VIT里, 而是图像直接输入到VIT里</font>**<font style="color:rgb(25, 27, 31);">。整体的结构图如下，可以看</font>**<font style="color:#ED740C;">到不同尺寸的图片可以有不同的image token个数</font>**<font style="color:rgb(25, 27, 31);">。其实背后的原理就是使用了</font>[<font style="color:rgb(9, 64, 142);">Patch n’ Pack</font>](https://zhida.zhihu.com/search?content_id=247800285&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)<font style="color:rgb(25, 27, 31);">: NaViT中的sequence packing技术。 </font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/2409.12191](https://arxiv.org/pdf/2409.12191)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://zhuanlan.zhihu.com/p/718515978](https://zhuanlan.zhihu.com/p/718515978)<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">每一个网络都有下采样倍数，那么输入的图像尺寸按理说应该是他的整数倍，能保证刚好被整除。以</font>[<font style="color:rgb(9, 64, 142);">qwen2vl</font>](https://zhida.zhihu.com/search?content_id=251439122&content_type=Article&match_order=1&q=qwen2vl&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（</font>[<font style="color:rgb(9, 64, 142);">vision backbone</font>](https://zhida.zhihu.com/search?content_id=251439122&content_type=Article&match_order=1&q=vision+backbone&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 下采样 28 倍）为例，</font>**<font style="color:#ED740C;">动态分辨率核心要考虑三个点：</font>**

1. <font style="color:rgb(25, 27, 31);">图像在resize的时候，既需要考虑图像尺寸是 28 的整数倍</font>
2. <font style="color:rgb(25, 27, 31);">也需要考虑尽可能的保证图像resize不失真，也就是</font>**<font style="color:#ED740C;">保持宽高比</font>**<font style="color:rgb(25, 27, 31);">。比如512x512的图像，如果resize 到了128x2048，那么图像就会严重失真。</font>
3. <font style="color:rgb(25, 27, 31);">其次就是训练的泛化性，推理的时候输入更小/大的图像（尤其视频帧），模型能不能外推。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742279868058-2c6afac1-6156-4b35-b85b-5fbd4f87edee.png)

:::color5
**<font style="color:#601BDE;">1.Qwen2-VL的动态分辨率 </font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(51, 51, 51);">动态分辨率</font>**<font style="color:rgb(51, 51, 51);">：与以往不同的是，Qwen2-VL 可以</font>**<font style="color:#74B602;">处理任意图像分辨率</font>**<font style="color:rgb(51, 51, 51);">，将其映射为动态数量的视token，提供更接近人类的视觉处理体验。</font>
    - **任意分辨率的图像**：取消[DFN ViT](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=DFN+ViT&zhida_source=entity)绝对位置编码，使用2d RoPE，使得ViT可以输入任意分辨率的图像。测试的时候，还会在后面接一个MLP，把2x2的token 编码成一个token。图像编码得到的token使用<|vision_start|> 和 <|vision_end|> 包裹。因此对于，224x224的图，因为ViT patch size=14，就会得到(224/14/2)^2+2 = 66 个token。**参考**：[多模态理解开源王者：InternVL 1.5->InternVL 2.0](https://zhuanlan.zhihu.com/p/707475931)
    - **图像Token范围**：qwen2-vl对图像token的范围，通过min_pixels和max_pixels 进行了约束，这两个变量描述了图像pixel的范围的最小值和最大值。如果小于或者大于min_pixels和max_pixels ，就会resize到这个范围内，以实现计算量和性能的trade off。<font style="color:#D22D8D;"> (by草莓师姐)</font>

```plain
MIN_PIXELS = 256*28*28
MAX_PIXELS = 512*28*28
```

    - **<font style="color:rgb(25, 27, 31);">训练泛化性</font>**<font style="color:rgb(25, 27, 31);">：根据qwen2vl提供的</font>[7B叙述](https://link.zhihu.com/?target=https%3A//huggingface.co/Qwen/Qwen2-VL-7B-Instruct/blob/main/preprocessor_config.json)<font style="color:rgb(25, 27, 31);">，min_pixel是3136，max_pixel是12845056，如何h和w一样大的话，</font>**<font style="color:#ED740C;">大概可以兼容从 56*56 到 3584x3584的图像输入</font>**<font style="color:rgb(25, 27, 31);">。但是对于video的每帧，考虑到多帧情况，最大是16384。并且由于scale到了min_pixels 和 max_pixels之间，所以泛化性不是问题。实际训练中也发现了，调整小max_pixel，对性能影响不大（不过这个也看啥任务）。</font>

:::color5
**<font style="color:#601BDE;">2.原生VIT逻辑 对比 Qwen2-VL的NaViT</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. **<font style="color:rgb(25, 27, 31);">原生的VIT</font>**<font style="color:rgb(25, 27, 31);">:	图片先resize到固定尺寸，比如VIT支持336 * 336尺寸的输入，我就先把图片先resize到336 * 336，然后分为n * n个Patch，每个Patch过Patch Embedding，然后再输入transformer layer中。但是比如下图这种情况，如果无脑resize效果肯定不太好，</font>**<font style="color:#74B602;">文字都被扭曲了</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. **<font style="color:rgb(25, 27, 31);">Qwen2-VL</font>**<font style="color:rgb(25, 27, 31);">:实现的</font>**<font style="color:rgb(25, 27, 31);">原生动态分辨率方法</font>**<font style="color:rgb(25, 27, 31);">则会保留原始图片的</font>**<font style="color:#74B602;">宽高比</font>**<font style="color:rgb(25, 27, 31);">，将图片resize到适当的大小，图片像素满足 </font><font style="color:rgb(25, 27, 31);">[min_pixel,max_pixel]</font><font style="color:rgb(25, 27, 31);"> 区间,再对图片做Patch处理，将每个图片处理成变长的Vision token序列，再输入给LLM模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742279439271-389336ce-176e-42e1-8745-3f69268bcf4a.png)

:::color5
**<font style="color:#601BDE;">2.Qwen2-VL动态分辨率逻辑</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL 对图像有4层处理逻辑：</font>

1. **Smart Resize**
2. **Rescale**
3. **Normalize**
4. **堆叠**

```python
# 第一步 resize 
if do_resize:
    resized_height, resized_width = smart_resize(
        height,
        width,
        factor=self.patch_size * self.merge_size,
        min_pixels=self.min_pixels,
        max_pixels=self.max_pixels,
    )
    image = resize(
        image, size=(resized_height, resized_width), resample=resample, input_data_format=input_data_format
    )

# 第二步 rescale 
if do_rescale:
    image = self.rescale(image, scale=rescale_factor, input_data_format=input_data_format)

# 第三步 normalize
if do_normalize:
    image = self.normalize(
        image=image, mean=image_mean, std=image_std, input_data_format=input_data_format
    )

# 第四步 堆叠...
```

1. **Smart Resize：**<font style="color:rgb(25, 27, 31);">分为两步：</font><font style="color:#D22D8D;"> (by草莓师姐)</font>
    1. <font style="color:rgb(25, 27, 31);">算宽高28的整数倍最接近的数值</font>

```python
h_bar = round(height / factor) * factor
w_bar = round(width / factor) * factor
```

    2. <font style="color:rgb(25, 27, 31);">统一放缩。这里有两个关键的参数</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">min_pixels</font>`<font style="color:rgb(25, 27, 31);">和</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">max_pixels</font>`<font style="color:rgb(25, 27, 31);">。这两个关键参数用来计量总的像素数，</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">pixels = hxw</font>`<font style="color:rgb(25, 27, 31);">。如果超过了max_pixels，那么就会统一resize到 min_pixels 和 max_pixels之间。</font>

```python
if h_bar * w_bar > max_pixels:
    beta = math.sqrt((height * width) / max_pixels)
    h_bar = math.floor(height / beta / factor) * factor
    w_bar = math.floor(width / beta / factor) * factor
```

2. **Rescale**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">这一步有一个关键的参数，rescale_factor。qwen2vl 默认取 0.00392156862745098（其实就是1/255），得到的结果就是 rescale_factor 逐元素相乘 image。</font>

```python
image = self.rescale(image, scale=rescale_factor, input_data_format=input_data_format)
```

3. **Normalize：**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">很传统的按照mean，std归一化。</font>

4. **堆叠：**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">因为qwen的vit最开始的embed方式是一个2x3x3的conv，所以需要把单图copy成2份，比如对于(1, 3, 924, 1232) 的图像就变成了(2, 3, 924, 1232)。</font>

```python
patches = np.tile(patches, (self.temporal_patch_size, 1, 1, 1))
```

### NaViT<font style="color:#D22D8D;"></font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">一般标准的预训练好的ViT，通常是将图片处理成正方形（长:宽=1:1）。这样处理后通常图片会失真，导致模型理解上有信息损失或引入一些误导。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">原生动态分辨率方法具体是怎么实现的呢？ 核心方法是采用了</font>**<font style="color:#ED740C;">NaViT的</font>**[**<font style="color:#ED740C;">Patch n’ Pack</font>**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**<font style="color:#ED740C;">技术，把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率</font>**<font style="color:rgb(25, 27, 31);">。同时在</font>**<font style="color:#ED740C;">一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐</font>**<font style="color:rgb(25, 27, 31);">，在性能上始终优于传统的ViT。</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/2307.06304](https://arxiv.org/pdf/2307.06304)

**参考：**[**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **[**24年下半年较新的VLM架构**](https://zhuanlan.zhihu.com/p/11503653276)<font style="color:#D22D8D;"> </font>

:::

:::color5
**<font style="color:#601BDE;">1.传统ViT 对比 NaViT</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **传统的ViT**：将任何图片数据都处理成定长的Patch序列，然后输入给Vision Encoder，这种统一定长的输入是对硬件计算非常友好的，非常好组Batch，并且不需要任何padding处理。Batch序列中每个位置的计算都是有效的。
+ **NaViT的**[**Patch n’ Pack**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**技术：把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率。同时在一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐，在性能上始终优于传统的ViT**。其性能提升主要来源于Pack处理后，一个序列包括多个图片能同时计算，使得在固定计算预算下，动态分辨率方法能训练更多样本，从而带来更好的性能。

:::color5
**<font style="color:#601BDE;">2.处理过程示例</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

**<font style="color:rgb(83, 88, 97);">举</font>****例**：假设我们5张图片： I<sub>1</sub>∼I<sub>5</sub> ，且patch长度为： 2∼6 ，即图片Patch后长度为： {I<sub>1</sub>:2, I<sub>2</sub>:3, I<sub>3</sub>:4, I<sub>4</sub>:5 , I<sub>5</sub>:6} 。为了描述简单，我们假设模型设置Batch_Size=2，并且正好处理这5张图片到一个Batch中。

1. **<font style="color:rgb(25, 27, 31);">将5张图片进行Pack，放到2个序列中</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">一个很简单的方式是将3个Patch较短的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> ，2个较长Patch的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);"> 。符号化为： </font><font style="color:rgb(25, 27, 31);">Batch={S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">,S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">}</font><font style="color:rgb(25, 27, 31);"> ，其中 </font><font style="color:rgb(25, 27, 31);">S1={I</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">:2,I</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">:3,I</font><sub><font style="color:rgb(25, 27, 31);">3</font></sub><font style="color:rgb(25, 27, 31);">:4}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">9</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">S2={I</font><sub><font style="color:rgb(25, 27, 31);">4</font></sub><font style="color:rgb(25, 27, 31);">:5,I</font><sub><font style="color:rgb(25, 27, 31);">5</font></sub><font style="color:rgb(25, 27, 31);">:6}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">11</font>

2. **<font style="color:rgb(25, 27, 31);">Batch内做序列Padding对齐处理</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">根据Batch内最长序列，通过F.pad方法做序列对齐，在序列前后增加Padding token，该例子中由于 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> 较短，需要在末尾增加Padding token，处理后，如下图所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742280392811-546c99ad-768a-447d-8ce8-2807a7dc9906.png)

3. **<font style="color:rgb(25, 27, 31);">通过设置Attention Mask保证同Sequence中各图片计算隔离</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

<font style="color:rgb(25, 27, 31);">一个序列中有多张图片输入，在计算时要必须保证各图片的Attention计算是相互隔离的。实现上通过对Attention Mask矩阵做特殊的设置，来保证计算隔离。计算Attention Mask的过程如下：</font>

<font style="color:rgb(25, 27, 31);">首先，记录序列中每个图片起止token位置（包括初始0位置），得到两个位置序列为：</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);">={0,2,5,9}</font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);">={0,5,11}</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);"> 中连续的两个数 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> 表示一张图片在序列中的长度为 </font><font style="color:rgb(25, 27, 31);">k−j</font><font style="color:rgb(25, 27, 31);"> 个特征，且特征的起止位置为： </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">k−1</font><font style="color:rgb(25, 27, 31);"> 。</font>

<font style="color:rgb(25, 27, 31);">然后，分别用 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);"> 来计算二维Attention mask矩阵，计算方式为：先初始化一个全0的mask矩阵，然后遍历每个 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);">，取 </font><font style="color:rgb(25, 27, 31);">[i,i+1]</font><font style="color:rgb(25, 27, 31);"> 位置的两个数字 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> ，使得矩阵行列坐标都满足在 </font><font style="color:rgb(25, 27, 31);">[j,k−1]</font><font style="color:rgb(25, 27, 31);"> 区间范围的位置置1。两个序列计算后的Mask矩阵，如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278208815-33fb8129-af9d-4c4a-bbb3-a0b220e4212a.png)

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">计算好了上面的Attention Mask矩阵，在过Vision Encoder网络时，</font>**<font style="color:#74B602;">将Attention Mask作用在Attention计算上，就会隔离同一序列中不同图像的Attention计算</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);"></font>

### <font style="color:rgb(25, 27, 31);">InternVL 1.5</font>
<font style="color:rgb(25, 27, 31);">动态分辨率：训练图像的分辨率从固定的 448×448 扩展到动态 448×448，其中patch大小为 448×448，patch数量范围为 1 到 12。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537741384-75721322-7fa4-4bca-97ce-e49a14ccff86.png)

1. **Pixel Shuffle**

<font style="color:rgb(25, 27, 31);">为了提高高分辨率下的可扩展性，我们简单地采用了</font>[**<font style="color:#74B602;">Pixel shuffle</font>**](https://zhida.zhihu.com/search?content_id=244382861&content_type=Article&match_order=1&q=Pixel+shuffle&zhida_source=entity)**<font style="color:#74B602;">操作，将视觉标记的数量减少到原来的四分之一</font>**<font style="color:rgb(25, 27, 31);">。因此，在我们的模型中，一幅 448×448 的图像由 256 个视觉标记表示。</font>

```python
def pixel_shuffle(self, x, scale_factor=0.5):
    n, w, h, c = x.size()
    # N, W, H, C --> N, W, H * scale, C // scale
    x = x.view(n, w, int(h * scale_factor), int(c / scale_factor))
    # N, W, H * scale, C // scale --> N, H * scale, W, C // scale
    x = x.permute(0, 2, 1, 3).contiguous()
    # N, H * scale, W, C // scale --> N, H * scale, W * scale, C // (scale ** 2)
    x = x.view(n, int(h * scale_factor), int(w * scale_factor),
               int(c / (scale_factor * scale_factor)))
    if self.ps_version == 'v1':
        warnings.warn("In ps_version 'v1', the height and width have not been swapped back, "
                      'which results in a transposed image.')
    else:
        x = x.permute(0, 2, 1, 3).contiguous()
    return x
```

2. **<font style="color:rgb(25, 27, 31);">动态宽高比匹配</font>**<font style="color:rgb(25, 27, 31);">：为了在处理过程中保持自然的宽高比，我们从一组预定义的宽高比中动态匹配最佳的宽高比。 由于计算资源有限，我们在训练期间</font>**<font style="color:#74B602;">最多允许 12 个patch</font>**<font style="color:rgb(25, 27, 31);">。 因此，该集合包括由 1 到 12 个patch形成的</font>**<font style="color:#74B602;">所有 35 种可能的宽高比组合，例如 {1:1、1:2、2:1、3:1、…、2:6}</font>**<font style="color:rgb(25, 27, 31);">。 在匹配过程中，对于每个输入图像，我们计算其纵横比，并通过</font>**<font style="color:#74B602;">测量绝对差将其与 35 个预定义的纵横比进行比较，选择最优宽高比</font>**<font style="color:rgb(25, 27, 31);">。 如果多个预定义的宽高比匹配(例如、1:1和2:2），我们会优先考虑不超过输入图像面积两倍的宽高比，从而防止低分辨率图像过度放大。</font>
3. **<font style="color:rgb(25, 27, 31);">图像resize</font>**<font style="color:rgb(25, 27, 31);">：一旦确定了适当的宽高比，图像的大小就会调整为相应的分辨率。 </font>**<font style="color:#74B602;">例如，800×1300 图像将调整为 896×1344</font>**<font style="color:rgb(25, 27, 31);">。 </font>
4. **<font style="color:rgb(25, 27, 31);">图像patch</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">调整大小的图像被分成 448×448 像素的图块</font>**<font style="color:rgb(25, 27, 31);">。 除了图块之外，</font>**<font style="color:#74B602;">我们还包含整个图像的缩略图以捕获全局上下文。 该缩略图缩小至 448×448</font>**<font style="color:rgb(25, 27, 31);">，帮助模型理解整个场景。</font>

```python
def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    # 获取原始图像尺寸和计算宽高比 
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # 生成目标宽高比集合：根据给定的最小值 (min_num) 和最大值 (max_num)，生成所有可能的目标宽高比组合 (i, j)，
    # 其中 i * j 在 [min_num, max_num] 范围内
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    
    # 对这些宽高比组合按面积排序，即按 i * j 排序
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # 找到最接近原始宽高比的目标宽高比，这里调用了辅助函数 find_closest_aspect_ratio
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # 计算目标图像的宽度和高度，根据目标宽高比和ViT的原生输入分辨率 (image_size：448) ，
    # 计算目标图像的宽度 (target_width) 和高度 (target_height），以及切图后的子图（448*448）数量
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # 根据计算结果resize
    resized_img = image.resize((target_width, target_height))
    # 将调整后的图像按照目标宽高比分割成多个小块，并存储在列表
    processed_images = []
    # 与Intern-VL不同的是，我的模型还需要动态分辨率模块输出每个子图的相对位置编号
    pos = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
        # 子图所在相对位置
        pos.append(i // (target_width // image_size), i % (target_width // image_size))
    # 检查子图数量是否正确
    assert len(processed_images) == blocks

    # 如果设置了 use_thumbnail 为 True 并且分割后的小块数量不是 1，则将原始图像调整为ViT原生输入大小的缩略图并添加到最后一个小块后面。
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images, pos
```

```python
def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        # 比较宽高比：将输入图像的宽高比与预定义的宽高比进行比较。比较的标准是计算绝对差异，
        # 即找到最接近输入图像宽高比的预定义宽高比
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        # 如果有多个预定义的宽高比与输入图像的宽高比相匹配（例如，1:1 和 2:2），系统会优先选择一个宽高比，
        # 该比率不会导致图像面积扩大超过输入图像面积的两倍。这是为了避免对低分辨率图像进行过度放大。
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    # print(f'width: {width}, height: {height}, best_ratio: {best_ratio}')
    return best_ratio
```



# 多模态大模型
一个典型的多模态大模型（MLLM）可以抽象为三个模块：（1）预训练的模态编码器；（2）预训练的大语言模型（LLM）；（3）跨模态投影层。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157259-d53bdda1-4e31-4694-b9a9-271570e2f749.png)

**视觉编码器**：通常视觉编码器不会总从头训练，一种常见的方法是使用已经与其他模态对齐的预训练编码器。例如，CLIP通过在图像-文本对上进行大规模预训练，将视觉编码器与文本在语义上对齐。下表总结了常用的图像编码器系列。除了普通的CLIP图像编码器，一些工作还探索了使用其他变体。例如，MiniGPT-4采用了EVA-CLIP（ViT-G/14）编码器，该编码器通过改进的训练技术进行训练。。一些工作还探索了无编码器架构，例如，Fuyu-8b的图像经过patch后直接经投影层后送到LLM。因此，该模型自然支持灵活的图像分辨率输入。

**预训练LLM**：通过在大量语料库上进行预训练，LLM已经嵌入了丰富的知识，并展示了强大的泛化和推理能力。我们在下表中总结了常用的LLM。大多数LLM属于因果解码器类别。其中，FlanT5系列是较早在BLIP-2和InstructBLIP等工作中使用的LLM。LLaMA系列和Vicuna家族是吸引了大量学术关注的代表性开源LLM。由于这两个LLM主要是在英语语料库上预训练的，它们在多语言支持方面受到限制，例如中文。

**跨模态投影层**：由于LLM只能感知文本，因此需要在自然语言和其他模态之间架起桥梁。然而，以端到端的方式训练大型多模态模型成本过高。更实际的方法是在预训练的视觉编码器和LLM之间引入一个可学习的连接器。可学习的连接器负责在不同模态之间架起桥梁。这种方法的代表是Q-Former。Q-Former利用一组可学习的query-token以基于查询的方式提取信息，首先在BLIP-2中实现。这种Q-Former风格的压缩视觉token到较少数量的表征向量。在参数大小方面，可学习的投影层参数通常只占编码器和LLM的一小部分。以Qwen-VL为例，Q-Former的参数大小约为0.08B，占整个参数的不到1%，而编码器和LLM分别占19.8%（1.9B）和80.2%（7.7B）。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157260-f5e090ef-3874-4dd7-ae82-7b34f204dc36.png)

开源方案

<font style="color:rgb(6, 6, 7);">自从GPT-4发布以来，多模态大模型展示了惊人的能力，MLLMs的研究热潮不断。下图展示了MLLMs的时间线。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472157255-8a21aa36-3ba1-4339-b0f5-d5f205a2b93f.png)





## GPT-4O<font style="color:#D22D8D;"></font>
:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">GPT-4o</font>](https://zhida.zhihu.com/search?content_id=243158209&content_type=Article&match_order=1&q=GPT-4o&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（omni,全部之意）是一个非常优秀的</font>[<font style="color:rgb(9, 64, 142);">多模态大模型</font>](https://zhida.zhihu.com/search?content_id=243158209&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。它的输入是语音、文字、图像/视频。输出自然有语音、文字、图像。</font>

**参考：**[**为什么说GPT-4o是原生多模态？**](https://www.zhihu.com/question/656277599/answer/3507582169)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935151830-5f5d1127-2e2d-4187-aa9a-c39f247e5418.png)

:::color5
**<font style="color:#601BDE;">1.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">从整体上看，GPT-4o是一个极其特殊的多模态模型。不太可能是多个模型组合的东西。所以，它的大概结构框架可能是这样的图。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935294342-353c1cd8-6a3f-4d8a-88e7-5a7865fec1aa.png)

:::color5
**<font style="color:#601BDE;">2.流式语音识别</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741935369990-a35e8166-c79f-4564-a36c-e46d7cfc56c2.png)

## 谷歌系列
### Gemma-3
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgba(0, 0, 0, 0.9);">在巴黎开发者日上，开源Gemma系模型正式迭代到第三代，原生支持多模态，128k上下文。</font>

<font style="color:rgba(0, 0, 0, 0.9);">此次，Gemma 3一共开源了四种参数，1B、4B、12B和27B。最最最关键的是，一块GPU/TPU就能跑模型。</font>

:::

:::color3
**简介：**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3是谷歌迄今最先进、最便携的开源模型，采用与Gemini 2.0模型相同的研究和技术打造。专为</font>**<font style="color:#ED740C;">在端侧设备上直接运行</font>**<font style="color:rgba(0, 0, 0, 0.9);">而设计——从手机和笔记本电脑到工作站，帮助开发者在需要的地方创建AI应用。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[gemma-3](https://huggingface.co/collections/google/gemma-3-release-67c6c6f89c4f76621268bb6d)

**paper：**[**Gemma 3 Technical Report**](https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf)

**参考：**[**谷歌Gemma 3上线！单GPU最强多模态手机可跑，27B完胜o3-mini**](https://mp.weixin.qq.com/s/buqtV1nEDhpvdvEFhRcoIA)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742207515480-2f0d38ab-e3d3-48e3-8ec2-7a0fb9f75fdf.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgba(0, 0, 0, 0.9);">使用世界最佳单设备加速模型进行开发：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3在LMArena排行榜的初步人类偏好评估中超越了Llama-405B、DeepSeek-V3和o3-mini，能在单个GPU或TPU主机上运行，开发独特的用户体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">支持140种语言，走向全球：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3为超过35种语言提供开箱即用的支持，并为超过140种语言提供预训练支持。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">创建具有高级文本和视觉推理能力的AI：</font>**<font style="color:rgba(0, 0, 0, 0.9);">轻松开发可以分析图像、文本和短视频的应用程序，为交互式和智能应用开创新的可能性。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">通过扩展的上下文窗口处理复杂任务：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3提供128k token的上下文窗口，让应用程序能够处理和理解海量信息。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用函数调用创建AI驱动的工作流：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3支持函数调用和结构化输出，帮助你实现任务自动化并构建智能体验。</font>
+ **<font style="color:rgba(0, 0, 0, 0.9);">使用量化模型更快实现高性能：</font>**<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3推出官方量化版本，在保持高精度的同时减少模型大小和计算需求。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">相比Gemma 2，研究者为Gemma 3预训练模型分配了更大的token预算。其中，Gemma 3 27B规模的模型在14万亿个token上进行训练，12B 规模的模型使用12T个token，4B 规模的模型使用4T个token，而1B规模的模型使用 2T个token。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **LLM：**

<font style="color:rgba(0, 0, 0, 0.9);">Gemma 3模型沿用了与前代版本相同的解码器Transformer 结构，其大部分架构元素与前两代Gemma版本类似。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了分组查询注意力（</font><font style="color:#74B602;">Grouped-Query Attention, GQA</font><font style="color:rgba(0, 0, 0, 0.9);">），并结合了</font>**<font style="color:#74B602;"> RMSNorm</font>**<font style="color:rgba(0, 0, 0, 0.9);">的后归一化（post-norm）和前归一化（pre-norm）。</font>

<font style="color:rgba(0, 0, 0, 0.9);">研究者在自注意力机制中交替使用局部</font>**<font style="color:#74B602;">滑动窗口自注意力</font>**<font style="color:rgba(0, 0, 0, 0.9);">和全局自注意力，按照5层局部层对应1层全局层的模式排列，模型的第一层为局部层。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在全局自注意力层上，研究者将</font>**<font style="color:#74B602;">RoPE的基准频率从10K提高到1M</font>**<font style="color:rgba(0, 0, 0, 0.9);">，而局部层的频率保持在10K。此外，他们采用了</font>**<font style="color:#74B602;">位置插值方法</font>**<font style="color:rgba(0, 0, 0, 0.9);">，以扩展全局自注意力层的适用范围。</font>

2. **视觉编码器：**

<font style="color:rgba(0, 0, 0, 0.9);">研究采用了一种</font>**<font style="color:#74B602;">400M规模的SigLIP编码器变体</font>**<font style="color:rgba(0, 0, 0, 0.9);">，这是一种基于Vision Transformer的模型，并使用CLIP损失的变体进行训练。Gemma视觉编码器的输入为调整尺寸后的896 × 896像素的方形图像，并在视觉助手任务的数据上进行微调。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在pre-train和post-train过程中，Gemma 3使用了蒸馏技术，并通过强化学习和模型合并的组合，进行了优化。</font>

<font style="color:rgba(0, 0, 0, 0.9);">在post-train阶段，使用多种奖励函数来提升模型在</font>**<font style="color:#74B602;">帮助性、数学、编程、推理、遵循指令和多语言</font>**<font style="color:rgba(0, 0, 0, 0.9);">能力方面的表现，同时最小化模型的有害性。Gemma 3主要使用了4个组件：</font>

+ <font style="color:rgba(0, 0, 0, 0.9);">从更大的指令模型中提取到Gemma 3预训练检查点</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">基于人类反馈的强化学习（RLHF），使模型预测与人类偏好保持一致。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">机器反馈强化学习（RLMF），增强数学推理。</font>
+ <font style="color:rgba(0, 0, 0, 0.9);">强化学习执行反馈（RLEF），提高编码能力。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

<font style="color:rgba(0, 0, 0, 0.9);">在多项基准测试中，Gemma 3全家桶相较于上一代实现了全面提升，27B模型在数学性能暴涨33-45分。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742206588016-d193937e-b4d6-4c3f-9343-5d250ea587be.png)





## Qwen-VL系列
### Qwen-VL系列对比<font style="color:#D22D8D;"></font>
:::color3
**参考：**[**如何评价千问发布的Qwen2.5-VL?**](https://www.zhihu.com/question/10742671583)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742194707977-e3d1a34f-e1f4-471a-a5e9-8fc0a97f03c2.png)

:::color5
**<font style="color:#601BDE;">1.模型结构对比</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| | **<font style="color:#000000;">Qwen-VL</font>** | **<font style="color:#000000;">Qwen2-VL</font>** | **<font style="color:#000000;">Qwen2.5-VL</font>** |
| --- | --- | --- | --- |
| 位置编码 | RoPE | <font style="color:#000000;">2D-RoPE, M-RoPE</font> | <font style="color:#000000;">2D-RoPE, M-RoPE</font> |
| 分辨率 | <font style="color:#000000;">预训练 224 x 224</font><br/><font style="color:#000000;">多任务预训练 448 x 448</font> | <font style="color:#000000;">动态分辨率</font> | <font style="color:#000000;">动态分辨率</font> |
| 视觉编码器 | <font style="color:rgb(25, 27, 31);">Openclip’s ViT-bigG</font> | <font style="color:rgb(25, 27, 31);">DFN-ViT + </font>[<font style="color:rgb(9, 64, 142);">2D RoPE</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=2D+RoPE&zhida_source=entity) | 1. <font style="color:rgb(25, 27, 31);">Dynamic-resolution ViT </font><br/>2. [<font style="color:rgb(9, 64, 142);">Window attention</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=Window+attention&zhida_source=entity)<br/>3. <font style="color:rgb(25, 27, 31);"> 2D RoPE</font> |
| <font style="color:rgb(25, 27, 31);">视觉编码器参数量</font> | <font style="color:rgb(25, 27, 31);">1.9B</font> | <font style="color:rgb(25, 27, 31);">675M</font> | <font style="color:rgb(25, 27, 31);">-</font> |
| <font style="color:rgb(25, 27, 31);">LLM</font> | <font style="color:rgb(25, 27, 31);">Qwen</font> | <font style="color:rgb(25, 27, 31);">Qwen2</font> | <font style="color:rgb(25, 27, 31);">Qwen2.5</font> |
| <font style="color:rgb(25, 27, 31);">多模态对齐</font> | [<font style="color:rgb(9, 64, 142);">Cross attention module</font>](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=Cross+attention+module&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> </font>**<font style="color:#ED740C;">（Q-former）</font>**<br/><font style="color:rgb(25, 27, 31);">visual feature不同size -> 256</font> | **<font style="color:#74B602;">Simple MLP</font>**<font style="color:rgb(25, 27, 31);">   </font><font style="color:rgb(25, 27, 31);">visual feature不同size -> 除以28</font> | **<font style="color:rgb(25, 27, 31);">两层MLP</font>**<font style="color:rgb(25, 27, 31);">   </font><font style="color:rgb(25, 27, 31);">visual feature不同size -> 除以28</font> |
| 归一化 |  |  | RMSNorm |
| 激活函数 |  |  | SwiGLU |
| 预训练 | 1. 预训练：冻结LLM，只优化了视觉编码器和VL适配器<br/>2. 多任务预训练：同时训练7项任务 | | 1. <font style="color:rgb(25, 27, 31);">视觉预训练</font><br/>2. <font style="color:rgb(25, 27, 31);">多模态预训练</font><br/>3. <font style="color:rgb(25, 27, 31);">长文本预训练</font> |
| SFT | 冻结视觉编码器，优化语言模型和适配器模块。 | | 动态配比优化机制 |
| DPO | / | |


### Qwen3-VL
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(0, 0, 0);">Qwen3VL的代码已于9月10号向HuggingFace的GitHub仓库提交PR，并在15号被合并。同时，据相关消息，其模型权重将在本周五（9月26号）的阿里云栖大会上发布。</font>

:::

:::color3
**简介：**<font style="color:rgb(0, 0, 0);">Qwen3-VL 是一个多模态视觉-语言模型系列，涵盖稠密（dense）与 MoE（稀疏专家）两类架构，并提供 Instruct 与 Thinking 版本。在前代基础上，</font>**<font style="color:#ED740C;">Qwen3-VL 在保持强劲纯文本能力的同时显著提升了视觉理解</font>**<font style="color:rgb(0, 0, 0);">。其关键架构改进包括：</font>

+ <font style="color:rgb(1, 1, 1);">采用交错布局（interleaved layout）的增强型MRoPE，用于更优的时空建模；</font>
+ <font style="color:rgb(1, 1, 1);">集成 DeepStack，有效利用 Vision Transformer（ViT）的多层级特征；</font>
+ <font style="color:rgb(1, 1, 1);">以及通过基于文本的时间对齐提升视频理解——从 T-RoPE 演进为“文本时间戳对齐”，实现更精确的时间定位。</font>

**github**：[Adding Support for Qwen3-VL Series](https://github.com/huggingface/transformers/pull/40795/commits/3860fcc43692d1cec9a31ea7e01a519beabdcfe9)

**huggingface**：[huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl#qwen3-vl](https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_vl#qwen3-vl)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[云栖大会](https://yunqi.aliyun.com/?spm=5176.30447480.J_kZCUqt4Y4-3pgz9RmjJMN.2.bfb93945hJZFJE)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758609927041-1aba8ed3-4e77-43d7-b6ba-f329f8163a61.png)

:::color5
**<font style="color:#601BDE;">1.引入DeepStack</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">在</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLVisionModel</font>`<font style="color:rgb(0, 0, 0);">中新引入</font>`<font style="color:rgb(239, 112, 96);">deepstack</font>`<font style="color:rgb(0, 0, 0);">模块。在默认config中，其会提取视觉编码器的第8, 16, 24层中间特征（默认config中视觉编码器总共27层）</font>

```python

class Qwen3VLVisionModel(Qwen3VLPreTrainedModel):
    def __init__(self, config, *inputs, **kwargs) -> None:
        ...
        self.deepstack_visual_indexes = config.deepstack_visual_indexes
        # deepstack_visual_indexes=[8, 16, 24]
        self.deepstack_merger_list = nn.ModuleList(
            [
                Qwen3VLVisionPatchMerger(
                    config=config,
                    use_postshuffle_norm=True,
                )
                for _ in range(len(config.deepstack_visual_indexes))
            ]
        )
        self.gradient_checkpointing = False
```

<font style="color:rgb(0, 0, 0);">这里的</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLVisionPatchMerger</font>`<font style="color:rgb(0, 0, 0);">是负责让视觉Token对齐到文本Token的MLP，与Qwen2.5VL架构中的</font>`<font style="color:rgb(239, 112, 96);">PatchMerger</font>`<font style="color:rgb(0, 0, 0);">功能类似，具体实现为：	</font>

```python
class Qwen3VLVisionPatchMerger(nn.Module):
    def __init__(self, config: Qwen3VLVisionConfig, use_postshuffle_norm=False) -> None:
        super().__init__()
        self.hidden_size = config.hidden_size * (config.spatial_merge_size**2)
        self.use_postshuffle_norm = use_postshuffle_norm
        self.norm = nn.LayerNorm(self.hidden_size if use_postshuffle_norm else config.hidden_size, eps=1e-6)
        self.linear_fc1 = nn.Linear(self.hidden_size, self.hidden_size)
        self.act_fn = nn.GELU()
        self.linear_fc2 = nn.Linear(self.hidden_size, config.out_hidden_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.norm(x.view(-1, self.hidden_size) if self.use_postshuffle_norm else x).view(-1, self.hidden_size)
        x = self.linear_fc2(self.act_fn(self.linear_fc1(x)))
        return x
```

<font style="color:rgb(0, 0, 0);">保存下来的</font>`<font style="color:rgb(239, 112, 96);">deepstack_feature_lists</font>`<font style="color:rgb(0, 0, 0);">会和</font>`<font style="color:rgb(239, 112, 96);">hidden_states</font>`<font style="color:rgb(0, 0, 0);">一起送到</font>`<font style="color:rgb(239, 112, 96);">Qwen3VLTextModel</font>`<font style="color:rgb(0, 0, 0);">(实际上用的就是Qwen3)，具体处理逻辑如下</font>

```python
class Qwen3VLTextModel(Qwen3VLPreTrainedModel):

    def __init__(self, config: Qwen3VLTextConfig):
        ...
        
    def forward(..., **kwargs ):
        # decoder layers
        for layer_idx, decoder_layer in enumerate(self.layers):
            layer_outputs = decoder_layer(
                hidden_states,
                attention_mask=attention_mask,
                position_ids=text_position_ids,
                past_key_values=past_key_values,
                cache_position=cache_position,
                position_embeddings=position_embeddings,
                **kwargs,
            )
            hidden_states = layer_outputs

            # add visual features to the hidden states of first several layers
            if deepstack_visual_embeds is not None and layer_idx in range(len(deepstack_visual_embeds)):
                hidden_states = self._deepstack_process(
                    hidden_states,
                    visual_pos_masks,
                    deepstack_visual_embeds[layer_idx],
                )

        hidden_states = self.norm(hidden_states)

        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=past_key_values,
        )
        
    def _deepstack_process(self, hidden_states, visual_pos_masks, visual_embeds):
        visual_pos_masks = visual_pos_masks.to(hidden_states.device)
        visual_embeds = visual_embeds.to(hidden_states.device, hidden_states.dtype)
        local_this = hidden_states[visual_pos_masks, :].clone() + visual_embeds
        hidden_states[visual_pos_masks, :] = local_this
        return hidden_states
```

<font style="color:rgb(0, 0, 0);">这里</font>`<font style="color:rgb(239, 112, 96);">visual_pos_masks</font>`<font style="color:rgb(0, 0, 0);">表示</font>`<font style="color:rgb(239, 112, 96);">hidden_states</font>`<font style="color:rgb(0, 0, 0);">中哪些token之前是视觉token。因此，上述操作就是在第8, 16, 24层中，直接把deepstack中保存的对应特征加到原本visual token的位置上，进行融合多尺度的特征。</font>

<font style="color:rgb(0, 0, 0);">实际上，这个结构与CV领域中常用的FPN在理念上非常相似。</font>

:::color5
**<font style="color:#601BDE;">2.基础配置改动</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">其中需要着重关注的是:</font>

1. <font style="color:rgb(1, 1, 1);">默认的hidden_act激活函数从</font>`<font style="color:rgb(239, 112, 96);">silu</font>`<font style="color:rgb(1, 1, 1);">替换为</font>`<font style="color:rgb(239, 112, 96);">gelu_pytorch_tanh</font>`
2. <font style="color:rgb(1, 1, 1);">视觉编码器中默认的patch_size由14x14变为16x16</font>

**Qwen3VL**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618299111-c9790b50-8977-45d7-b724-19595f534ef0.png)

**Qwen2.5VL**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618267869-6cf629bd-faea-44e6-988f-595a45080a0f.png)

:::color5
**<font style="color:#601BDE;">3.视频处理逻辑修改</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

`<font style="color:rgb(239, 112, 96);">Qwen3VLProcessor</font>`<font style="color:rgb(0, 0, 0);">中的图像处理和tokenizer与Qwen2.5VL相同，继续沿用Qwen2中的</font>`<font style="color:rgb(239, 112, 96);">Qwen2VLImageProcessor</font>`<font style="color:rgb(0, 0, 0);">和</font>`<font style="color:rgb(239, 112, 96);">Qwen2TokenizerFast</font>`<font style="color:rgb(0, 0, 0);">。</font>

```python
class Qwen3VLProcessor(ProcessorMixin):
    r"""
    Constructs a Qwen3VL processor which wraps a Qwen3VL image processor and a Qwen2 tokenizer into a single processor.
    [`Qwen3VLProcessor`] offers all the functionalities of [`Qwen2VLImageProcessor`] and [`Qwen2TokenizerFast`]. See the
    [`~Qwen3VLProcessor.__call__`] and [`~Qwen3VLProcessor.decode`] for more information.
    Args:
        image_processor ([`Qwen2VLImageProcessor`], *optional*):
            The image processor is a required input.
        tokenizer ([`Qwen2TokenizerFast`], *optional*):
            The tokenizer is a required input.
        video_processor ([`Qwen3VLVideoProcessor`], *optional*):
            The video processor is a required input.
        chat_template (`str`, *optional*): A Jinja template which will be used to convert lists of messages
            in a chat into a tokenizable string.
    """

    attributes = ["image_processor", "tokenizer", "video_processor"]
    image_processor_class = "AutoImageProcessor"
    video_processor_class = "AutoVideoProcessor"
    tokenizer_class = ("Qwen2Tokenizer", "Qwen2TokenizerFast")
```

<font style="color:rgb(0, 0, 0);">但在视频处理中，本次</font>**<font style="color:rgb(0, 0, 0);">引入了新的Qwen3VLVideoProcessor</font>**<font style="color:rgb(0, 0, 0);">。其重新实现了</font>`<font style="color:rgb(239, 112, 96);">smart_resize</font>`<font style="color:rgb(0, 0, 0);">函数，从仅按空间分辨率(H,W)约束，升级为按时空体素(T×H×W)的总像素预算做“THW 联动”缩放，更适配视频处理:</font>

```python
def smart_resize(
    num_frames: int,
    height: int,
    width: int,
    temporal_factor: int = 2,
    factor: int = 32,
    min_pixels: int = 128 * 128,
    max_pixels: int = 16 * 16 * 2 * 2 * 2 * 6144,
):
    if num_frames < temporal_factor:
        raise ValueError(f"t:{num_frames} must be larger than temporal_factor:{temporal_factor}")
    if height < factor or width < factor:
        raise ValueError(f"height:{height} or width:{width} must be larger than factor:{factor}")
    elif max(height, width) / min(height, width) > 200:
        raise ValueError(
            f"absolute aspect ratio must be smaller than 200, got {max(height, width) / min(height, width)}"
        )
    h_bar = round(height / factor) * factor
    w_bar = round(width / factor) * factor
    t_bar = round(num_frames / temporal_factor) * temporal_factor

    if t_bar * h_bar * w_bar > max_pixels:
        beta = math.sqrt((num_frames * height * width) / max_pixels)
        h_bar = max(factor, math.floor(height / beta / factor) * factor)
        w_bar = max(factor, math.floor(width / beta / factor) * factor)
    elif t_bar * h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (num_frames * height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar
```

:::color5
**<font style="color:#601BDE;">4.</font>****<font style="color:#601BDE;">T-RoPE改为时间戳对齐</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">此外，本次改动将T-RoPE改为时间戳对齐。原本的Qwen2.5VL是用绝对时间id+动态fps实现的T-RoPE，而Qwen3VL改成了对每帧利用文本时间戳去确定RoPE，核心代码区别如下：</font>

[modeling_qwen3_vl.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_vl/modeling_qwen3_vl.py)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1758618747395-60b51954-2850-4228-b8d6-5a40f94ce97c.png)

:::color5
**<font style="color:#601BDE;">5.M-ROPE改进</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(0, 0, 0);">Qwen2-VL为了适应多模态输入引入了M-RoPE，对所有模态进行统一编码，这个模块也被延用到Qwen2.5VL。</font>

<font style="color:rgb(0, 0, 0);">M-RoPE把所有模态的数据都看作有3个维度</font><font style="color:rgb(1, 1, 1);">(T, H, W)</font><font style="color:rgb(0, 0, 0);">，具体来说：</font>

+ <font style="color:rgb(1, 1, 1);">对于视频的话，每一帧的T的index是往后递增的；</font>
+ <font style="color:rgb(0, 0, 0);">对于单张图片来说T的index是不动的，HW随着位置变化会变二维index；</font>
+ <font style="color:rgb(1, 1, 1);">对于文本来说，(T, H, W)默认都是相等的。</font>

<font style="color:rgb(0, 0, 0);">而在Qwen3VL中，把三维频率从分块布局[TTT...HHH...WWW]重排成交替布局[THTHWHTW]，实现“交织式”的多模态RoPE。</font>

```python
class Qwen3VLTextRotaryEmbedding(nn.Module):
    def __init__(self, config: Qwen3VLTextConfig, device=None):
    ...
    
    def apply_interleaved_mrope(self, freqs, mrope_section):
        """Apply interleaved MRoPE to 3D rotary embeddings.
        Reorganizes frequency layout from chunked [TTT...HHH...WWW] to
        interleaved [THTHWHTHW...TT], preserving frequency continuity.
        args:
            x: (3, bs, seq_len, head_dim // 2)
            mrope_section: (3,)
        returns:
            x_t: (bs, seq_len, head_dim // 2)
        """
        freqs_t = freqs[0]  # just overwrite the first dimension T
        for dim, offset in enumerate((1, 2), start=1):  # H, W
            length = mrope_section[dim] * 3
            idx = slice(offset, length, 3)
            freqs_t[..., idx] = freqs[dim, ..., idx]
        return freqs_t
```

### Qwen2.5-VL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(31, 31, 31);"></font>**<font style="color:rgb(31, 31, 31);">Qwen2.5-VL</font>**<font style="color:rgb(31, 31, 31);">，Qwen 模型家族的旗舰视觉语言模型，包含 3B、7B 和 72B  3 个模型尺寸。</font>

:::

:::color3
**简介：****<font style="color:rgb(31, 31, 31);">Qwen2.5-VL的主要特点：</font>**

+ **<font style="color:rgb(31, 31, 31);">感知更丰富的世界</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 不仅擅长识别常见物体，如花、鸟、鱼和昆虫，还能够分析图像中的文本、图表、图标、图形和布局。</font>
+ **<font style="color:rgb(31, 31, 31);">Agent</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 直接作为一个视觉 Agent，可以推理并动态地使用工具，初步具备了使用电脑和使用手机的能力。</font>
+ **<font style="color:rgb(31, 31, 31);">理解长视频和捕捉事件</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 能够理解超过 1 小时的视频，并且这次它具备了通过精准定位相关视频片段来捕捉事件的新能力。</font>
+ **<font style="color:rgb(31, 31, 31);">视觉定位</font>**<font style="color:rgb(31, 31, 31);">：Qwen2.5-VL 可以通过生成 bounding boxes 或者 points 来准确定位图像中的物体，并能够为坐标和属性提供稳定的 JSON 输出。</font>
+ **<font style="color:rgb(31, 31, 31);">结构化输出</font>**<font style="color:rgb(31, 31, 31);">：对于发票、表单、表格等数据，Qwen2.5-VL 支持其内容的结构化输出，惠及金融、商业等领域的应用。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://qwenlm.github.io/zh/blog/qwen2.5-vl/](https://qwenlm.github.io/zh/blog/qwen2.5-vl/)

**github**：[https://github.com/QwenLM/Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583)  [Qwen2.5-VL更新！](https://zhuanlan.zhihu.com/p/25347969116)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191876384-65f80eeb-919a-4f47-990e-48e0f7b6ba3e.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">算法侧提升</font>**

+ **<font style="color:rgb(25, 27, 31);">Vision encoder</font>**
    - <font style="color:rgb(25, 27, 31);">使用了_</font>[<font style="color:rgb(9, 64, 142);">window attention</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=window+attention&zhida_source=entity)<font style="color:rgb(25, 27, 31);">_ 提高inference效率</font>
+ **<font style="color:rgb(25, 27, 31);">Video understanding</font>**
    - <font style="color:rgb(25, 27, 31);">引入了 dynamic FPS sampling 策略，相当于一种时间上的dynamic resolution</font>
    - <font style="color:rgb(25, 27, 31);">升级了</font>[<font style="color:rgb(9, 64, 142);">MRoPE</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=MRoPE&zhida_source=entity)<font style="color:rgb(25, 27, 31);">在时间上，对齐了 absolute time</font>
+ **<font style="color:rgb(25, 27, 31);">High-Qaulity Data</font>**
    - <font style="color:rgb(25, 27, 31);">从1.2 trillion 数据增加到 4.1 trillion 数据（单位token）</font>

**<font style="color:rgb(25, 27, 31);">应用侧展现</font>**

+ **<font style="color:rgb(25, 27, 31);">强大的文档解析能力:</font>**
    - <font style="color:rgb(25, 27, 31);">升级文本识别至全文档解析 (</font>[<font style="color:rgb(9, 64, 142);">Omnidocument Parsing</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=Omnidocument+Parsing&zhida_source=entity)<font style="color:rgb(25, 27, 31);">)。</font>
    - <font style="color:rgb(25, 27, 31);">擅长处理多场景、多语言文档。</font>
    - <font style="color:rgb(25, 27, 31);">支持内置内容类型：手写、表格、图表、化学公式、乐谱。</font>
+ **<font style="color:rgb(25, 27, 31);">精确的跨格式对象定位:</font>**
    - <font style="color:rgb(25, 27, 31);">显著提升</font>**<font style="color:rgb(25, 27, 31);">物体检测</font>**<font style="color:rgb(25, 27, 31);">、</font>**<font style="color:rgb(25, 27, 31);">pointing</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font>**<font style="color:rgb(25, 27, 31);">计数</font>**<font style="color:rgb(25, 27, 31);">精度。</font>
    - <font style="color:rgb(25, 27, 31);">支持输出物体坐标和JSON格式，实现高级空间推理。【除了box，增加point定位物体能力，并能稳定输出json】</font>
+ **<font style="color:rgb(25, 27, 31);">超长视频理解与细粒度视频定位:</font>**
    - <font style="color:rgb(25, 27, 31);">动态分辨率扩展至时间维度。</font>
    - <font style="color:rgb(25, 27, 31);">能够理解数小时的视频。【并非算法提升】</font>
    - <font style="color:rgb(25, 27, 31);">可以秒级提取视频片段。【Qwen2-VL已经有了】</font>
+ **<font style="color:rgb(25, 27, 31);">增强的智能体（agent）功能:</font>**
    - <font style="color:rgb(25, 27, 31);">利用高级定位、推理和决策能力。</font>
    - <font style="color:rgb(25, 27, 31);">适用于计算机和移动设备。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">Qwen2.5-VL 其实大部分的篇幅在数据处理，也就是SFT时代最枯燥但是最有用的工作。。。</font>**

<font style="color:rgb(25, 27, 31);">简单来说其预训练阶段采用</font>**<font style="color:rgb(25, 27, 31);">4万亿token</font>**<font style="color:rgb(25, 27, 31);">的高质量数据集，相比前代模型数据规模提升3倍以上，覆盖</font>**<font style="color:rgb(25, 27, 31);">图像描述、交错图文、OCR识别、视觉知识、文档解析、视频理解、智能体交互</font>**<font style="color:rgb(25, 27, 31);">等十余种模态类型。为确保不同模态数据的协同效应，千问团队提出一种</font>**<font style="color:#74B602;">动态配比优化机制</font>**<font style="color:rgb(25, 27, 31);">，避免模态之间冲突。这里就不展开了，主要是因为数据处理太垂直了，每一批数据都有tricky解法。</font>

**<font style="color:rgb(25, 27, 31);">预训练训练数据如下：</font>**<font style="color:rgb(25, 27, 31);">	</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192466068-c99ae061-5eed-44ad-b579-8881737b4aa9.png)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2.5-VL的结构改造重点就是</font>[<font style="color:rgb(9, 64, 142);">ViT</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=ViT&zhida_source=entity)<font style="color:rgb(25, 27, 31);">的改进。</font>

1. **<font style="color:rgb(25, 27, 31);">window attention</font>**

<font style="color:rgb(25, 27, 31);">基于ViT，Qwen2.5-VL使用了 window attention 编码图像加速计算。window attention 在swin transformer时代已经被广泛验证了其有效性了。</font>**<font style="color:#ED740C;">Window Attention将输入分割成不重叠的局部窗口，并在每个窗口内独立计算自attention</font>**<font style="color:rgb(25, 27, 31);">。之后会有一个</font>**<font style="color:#74B602;">shift window的操作，把每一个局部的attention关联为全局的attention</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">具体的，仅有四个 layers 使用 full self-attention，其余 layers 使用 windowed attention（最大 window size 为 112x112，对应 8x8 patches，因为这里image patche是14x14的pixels）。小于 112x112 的区域不进行 padding，以原始分辨率处理。这种设计使得模型能够直接处理原始分辨率的 input，避免不必要的 scaling 和 distortion。</font>

2. **<font style="color:rgb(25, 27, 31);">归一化</font>**<font style="color:rgb(25, 27, 31);">：使用</font>[<font style="color:rgb(9, 64, 142);">RMSNorm</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=RMSNorm&zhida_source=entity)<font style="color:rgb(25, 27, 31);">归一化</font>
3. **<font style="color:rgb(25, 27, 31);">激活函数</font>**<font style="color:rgb(25, 27, 31);">：使用SwiGLU做激活函数。</font>
4. **<font style="color:rgb(25, 27, 31);">training from scratch</font>**
    1. <font style="color:rgb(25, 27, 31);">由于RoPE和window attention等组件引入，整个ViT重新训练了。包含三个训练阶段，具体的细节没有展开</font>
    2. [<font style="color:rgb(9, 64, 142);">CLIP pre-training</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=CLIP+pre-training&zhida_source=entity)
    3. <font style="color:rgb(25, 27, 31);">vision-language alignment</font>
    4. [<font style="color:rgb(9, 64, 142);">end-to-end fine-tuning</font>](https://zhida.zhihu.com/search?content_id=254091776&content_type=Article&match_order=1&q=end-to-end+fine-tuning&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。</font>
5. **<font style="color:rgb(25, 27, 31);">LLM</font>**<font style="color:rgb(25, 27, 31);">：引入了 Qwen2.5 LLM，唯一需要修改的就是把原来一维的RoPE改为 MRoPE</font>
6. <font style="color:rgb(25, 27, 31);">多模态对齐（多模态adaptor）：这里的MLP映射没变，主要考虑了vision 的token太多了，所以需要压缩送入LLM。所以最后用了</font>**<font style="color:#74B602;">两层MLP压缩vision token四倍</font>**<font style="color:rgb(25, 27, 31);">（2x2）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练：**<font style="color:rgb(25, 27, 31);">整个训练可以划分为三个阶段：</font>
    1. **<font style="color:rgb(25, 27, 31);">第一阶段，视觉预训练</font>**<font style="color:rgb(25, 27, 31);">，奠定 multimodal 理解的基础，主要使用 </font>**<font style="color:#74B602;">image captions、visual knowledge 和 OCR data</font>**<font style="color:rgb(25, 27, 31);">。这些数据集帮助 ViT 提取有效的视觉表征，并与 textual information 整合。</font>
    2. **<font style="color:rgb(25, 27, 31);">第二阶段，多模态预训练</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">解冻所有 model 参数</font>**<font style="color:rgb(25, 27, 31);">，使用多样化的 multimodal image data 进行训练。这一阶段引入更复杂的数据集，如</font>**<font style="color:#74B602;"> interleaved data、multi-task learning datasets、VQA、multimodal mathematics、agent-based tasks、video understanding 和 pure-text datasets</font>**<font style="color:rgb(25, 27, 31);">，增强模型在视觉和语言模态间建立深层联系的能力，能够处理更复杂的任务。</font>
    3. **<font style="color:rgb(25, 27, 31);">第三阶段，长文本预训练</font>**<font style="color:rgb(25, 27, 31);">，进一步提升模型在</font>**<font style="color:#74B602;">长序列、video 和 agent-based data 上的推理能力</font>**<font style="color:rgb(25, 27, 31);">，同时增加 sequence length。这使模型能够处理更高级和精细的 multimodal 任务，特别适用于需要长距离依赖和复杂推理的任务。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192466068-c99ae061-5eed-44ad-b579-8881737b4aa9.png)

2. **SFT+DPO：**

<font style="color:rgb(25, 27, 31);">在Supervised Fine-Tuning (SFT)阶段，千问团队采用了一个精心策划的数据集，以提升模型在多种模态下的指令遵循能力。该数据集约包含</font>**<font style="color:rgb(25, 27, 31);">200万条条目，50%为纯文本数据，50%为多模态数据</font>**<font style="color:rgb(25, 27, 31);">，包括</font>**<font style="color:rgb(25, 27, 31);">image-text和video-text组合</font>**<font style="color:rgb(25, 27, 31);">。多模态数据由于包含视觉和时间信息，训练时消耗的tokens和计算资源显著更多。</font>**<font style="color:rgb(25, 27, 31);">数据集主要由中文和英文数据组成</font>**<font style="color:rgb(25, 27, 31);">，并辅以多语言条目以支持更广泛的语言多样性。</font>

<font style="color:rgb(25, 27, 31);">为了适应多种应用场景，数据集包含专门的子集，如General Visual Question Answering (VQA)、image captioning、数学问题解决、coding任务和security-related queries。此外，还构建了专门用于Document和Optical Character Recognition (Doc and OCR)、Grounding、Video Analysis以及Agent Interactions的数据集，以提升领域特定的能力。这里还有详细的过滤流程，还是一样，有兴趣可以看原文。</font>

:::color5
**<font style="color:#601BDE;">5.</font>****<font style="color:#601BDE;">原生动态分辨率和帧率</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">这里Qwen2.5-VL介绍了两个概念：dynamic frame rate 和 absolute time encoding。</font>

<font style="color:rgb(25, 27, 31);">我们知道对于很多Video generation的工作，为了让网络知道FPS的概念，timestamps是文本形式（字符串）通过text encoder 编码进入网络的然后一般cross attention一下。</font>

<font style="color:rgb(25, 27, 31);">这里千问团队采用的是直接将MRoPE的ID和timestamp对齐，那么就可以动态采样MRoPE的ID来采样不同FPS的视频了， 所以也就不需要额外编码timestamp了，因为天然的是对齐的。如下图，因为qwen是用一个</font>**<font style="color:#ED740C;">2x3x3的3d conv编码的，所以一秒编码两帧，刚好就是两个MRoPE的ID</font>**<font style="color:rgb(25, 27, 31);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742192956900-8b6751b1-a6b7-4fd6-948e-b44b4a59491d.png)

:::color5
**<font style="color:#601BDE;">6.模型评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(31, 31, 31);">72B:</font>**

<font style="color:rgb(31, 31, 31);">我们对视觉语言模型进行了全面的评估，比较了 SOTA 模型以及同尺寸规模模型中表现最好的模型。在旗舰模型 Qwen2.5-VL-72B-Instruct 的测试中，它在一系列涵盖多个领域和任务的基准测试中表现出色，包括大学水平的问题、数学、文档理解、视觉问答、视频理解和视觉 Agent。值得注意的是，Qwen2.5-VL 在理解文档和图表方面具有显著优势，并且能够作为视觉 Agent 进行操作，而无需特定任务的微调。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182471383-34f20b80-bc3d-4198-8879-61ea4f3d0a6f.png)

2. **<font style="color:rgb(31, 31, 31);">7B:</font>**

<font style="color:rgb(31, 31, 31);">在较小的模型方面，Qwen2.5-VL-7B-Instruct 在多个任务中超越了 GPT-4o-mini</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182438789-c0905007-48fa-448b-8ae6-a2b3388cf401.png)

3. **<font style="color:rgb(31, 31, 31);">3B:</font>**

<font style="color:rgb(31, 31, 31);">Qwen2.5-VL-3B 作为端侧 AI 的潜力股，甚至超越了我们之前版本 Qwen2-VL 的 7B 模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742182457958-577639f4-3f09-4d04-bcd5-4cce4c050062.png)

### Qwen2-VL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介**：作为在Qwen-VL基础上迭代的最新版本，Qwen2-VL在视觉理解上达到非常先进的性能。**<font style="color:#ECAA04;">不再使用Q-former,而是直接使用MLP进行对齐。</font>**

**paper : **[**https://arxiv.org/pdf/2409.12191**](https://arxiv.org/pdf/2409.12191)

**项目地址**：[https://github.com/QwenLM/Qwen2-VL](https://github.com/QwenLM/Qwen2-VL)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583) [**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **

:::

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1733472157254-037f1f85-1f1b-4cf5-8fc7-24d39969869f.jpeg)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(51, 51, 51);">对各种分辨率和比例的图像的先进理解</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 在视觉理解基准上达到最先进的性能，包括 MathVista、DocVQA、RealWorldQA、MTVQA 等。</font>
+ **<font style="color:rgb(51, 51, 51);">理解超过 20 分钟的视频</font>**<font style="color:rgb(51, 51, 51);">：Qwen2-VL 能够处理超过 20 分钟的视频，提供高质量的视频问答、对话、内容创作等功能。</font>
+ **<font style="color:rgb(51, 51, 51);">可操作手机、机器人等设备的智能体</font>**<font style="color:rgb(51, 51, 51);">：具备复杂推理和决策能力的 Qwen2-VL 可以与手机、机器人等设备集成，基于视觉环境和文本指令进行自动操作。</font>
+ **<font style="color:rgb(51, 51, 51);">多语言支持</font>**<font style="color:rgb(51, 51, 51);">：为了服务全球用户，Qwen2-VL 除了支持英语和中文外，现在还能够理解图像中不同语言的文本，包括大多数欧洲语言、日语、韩语、阿拉伯语、越南语等。</font>

:::color5
**<font style="color:#601BDE;">2.模型架构更新</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **视觉、文本编码器升级：**
    - **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：之前qwenvl用的Openclip’s ViT-bigG-14，现在用的是</font>**<font style="color:#ED740C;">DFN的ViT</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - **<font style="color:rgb(25, 27, 31);">LLM</font>**<font style="color:rgb(25, 27, 31);">：升级到了Qwen2，值得注意的是对于不同大小的LLM，vision encoder 参数量不变。</font>
2. **<font style="color:rgb(51, 51, 51);">动态分辨率</font>**<font style="color:rgb(51, 51, 51);">：与以往不同的是，Qwen2-VL 可以</font>**<font style="color:#74B602;">处理任意图像分辨率</font>**<font style="color:rgb(51, 51, 51);">，将其映射为动态数量的视token，提供更接近人类的视觉处理体验。</font>
    - **任意分辨率的图像**：取消[DFN ViT](https://zhida.zhihu.com/search?content_id=717519310&content_type=Answer&match_order=1&q=DFN+ViT&zhida_source=entity)绝对位置编码，使用2d RoPE，使得ViT可以输入任意分辨率的图像。测试的时候，还会在后面接一个MLP，把2x2的token 编码成一个token。图像编码得到的token使用<|vision_start|> 和 <|vision_end|> 包裹。因此对于，224x224的图，因为ViT patch size=14，就会得到(224/14/2)^2+2 = 66 个token。**参考**：[多模态理解开源王者：InternVL 1.5->InternVL 2.0](https://zhuanlan.zhihu.com/p/707475931)
    - **图像Token范围**：qwen2-vl对图像token的范围，通过min_pixels和max_pixels 进行了约束，这两个变量描述了图像pixel的范围的最小值和最大值。如果小于或者大于min_pixels和max_pixels ，就会resize到这个范围内，以实现计算量和性能的trade off。

```plain
MIN_PIXELS = 256*28*28
MAX_PIXELS = 512*28*28
```

3. **<font style="color:rgb(51, 51, 51);">多模态旋转位置嵌入 (M-ROPE)</font>**<font style="color:rgb(51, 51, 51);">：将位置嵌入分解为多个部分，</font>**<font style="color:#74B602;">以捕捉 1D 文本、2D 视觉和 3D 视频的位置信息</font>**<font style="color:rgb(51, 51, 51);">，增强其多模态处理能力。</font><font style="color:rgb(25, 27, 31);">在空间分辨率上，增加了</font>**<font style="color:#ED740C;">时间维度</font>**<font style="color:rgb(25, 27, 31);">，如果是文本，三个分量都相同。消融实验证明M-RoPE在下游效果更好。</font>**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[从浅到深入门旋转位置编码](https://zhuanlan.zhihu.com/p/13023539180)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191399043-bf846218-c884-419e-8b74-7b79077e7890.png)

4. **<font style="color:rgb(25, 27, 31);">统一的图像、视频理解</font>**

<font style="color:rgb(25, 27, 31);">为了更好理解视频，使用</font>**<font style="color:#ED740C;">时间轴为2的3d conv编码图像/视频</font>**<font style="color:rgb(25, 27, 31);">。具体来说，如果是一张图，就copy两份，如果是视频就每秒采样2帧。</font>

5. **Bounding box 坐标归一化**

之前Qwen1-VL 的 bounding box是绝对坐标，而Qwen2-VL是归一化坐标，虽然叫归一化坐标，但是实际上是归一化到了[0, 1000)，坐标就是![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742191763591-d922011a-c86e-4df5-b65c-9fb8daeadde3.png)的形式。格式就像这样，被检测的物体和box坐标分别被speical token包裹。

```python
<|object_ref_start|>the eyes on a giraffe<|object_ref_end|><|box_start|>(176,106),(232,160)<|box_end|>
```

6. **Visual Agent**

Visual agent 就是function call 的能力，让LLM直接调用某个function并输入参数，Qwen2-VL中支持了这一个操作。

:::color5
**<font style="color:#601BDE;">3.多模态Adaptor：MLP</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL采用了一种更简单的压缩方法：对</font>**<font style="color:#74B602;">空间位置临近的patch 特征做拼接，再经过2层MLP线性变换</font>**<font style="color:rgb(25, 27, 31);">，这样将原来长度为 </font><font style="color:rgb(25, 27, 31);">n</font><font style="color:rgb(25, 27, 31);"> 的序列，可压缩到 </font><font style="color:rgb(25, 27, 31);">n/4</font><font style="color:rgb(25, 27, 31);"> ，最终将压缩后的特征序列输入给LLM模型。处理过程如下图所示：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278493947-67adfde1-1e94-48d0-8b71-8cde17fd7ad8.png)

**<font style="color:rgb(25, 27, 31);">Vision token</font>**

<font style="color:rgb(25, 27, 31);">为了区分Vision token和文本token，Qwen2-VL也引入了两个特殊的token </font><font style="color:rgb(25, 27, 31);"><|vision_start|></font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);"><|vision_end|></font><font style="color:rgb(25, 27, 31);"> 来标识Vision token。</font>

```python
对于一个 224x224 ，如果ViT的 patch_size = 14 ，最终将图片编码成一个66个token的序列输入到模型。
具体计算过程：
1.Patch 处理后的Token数为： (224/14) x (224/14) = 16x16 = 256
2.经过输入投影层压缩处理： 256/4 = 64
3. 最后再加上 2 个起止位置的特殊token： 64+2 = 66

```

**为什么不用Q-Former？**

<font style="color:rgb(25, 27, 31);">主要是因为Cross-Attention架构适合处理</font>**<font style="color:#74B602;">固定长度的 </font>****<font style="color:#74B602;">k,v</font>****<font style="color:#74B602;"> </font>**<font style="color:rgb(25, 27, 31);">，当 </font><font style="color:rgb(25, 27, 31);">k,v</font><font style="color:rgb(25, 27, 31);"> 长短不一时，是不适合做Attention计算的。而Qwen2-VL通过原生动态分辨率方法处理的每个图片的token序列恰恰是变长的，无法使用Cross-Attention架构做特征压缩处理。</font>

:::color5
**<font style="color:#601BDE;">4.统一的图像&视频理解框架</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">Qwen2-VL统一了视频和图像的理解框架，能混合输入图像和视频数据进行理解。为了保证图片和视频的处理一致，对视频和图像分别做如下处理：</font>

+ **<font style="color:rgb(25, 27, 31);">视频处理：</font>**<font style="color:rgb(25, 27, 31);">以</font>**<font style="color:#74B602;">每秒两帧的速率对视频进行采样</font>**<font style="color:rgb(25, 27, 31);">，最终可采样偶数个帧序列。对于长视频为了平衡序列长度和计算效率，通过动态调整每一帧的分辨率，将视频总token限制在16K以内。</font>
+ **<font style="color:rgb(25, 27, 31);">图像处理：</font>**<font style="color:rgb(25, 27, 31);">对图像做复制操作，使得单一图片，变成一个</font>**<font style="color:#74B602;">时序为2的帧序列</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">使用3D的卷积对帧序列做特征抽取，如下图所示，每两张图片为一组进行卷积操作抽取特征。这样通过将卷积核扩充了时序维度，可以进一步压缩序列长度，因此也能进一步提升模型处理更多帧的能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742280064072-3de7c797-cd76-4fd2-9006-2b768ba27b66.png)

### Qwen-VL
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">QWEN-VL是阿里巴巴达摩院开发的</font>**<font style="color:rgb(51, 51, 51);">多模态大语言模型</font>**<font style="color:rgb(51, 51, 51);">（MLLM），支持</font>**<font style="color:rgb(51, 51, 51);">视觉-语言联合理解</font>**<font style="color:rgb(51, 51, 51);">。其背景特点包括：</font>

+ **<font style="color:rgb(51, 51, 51);">行业需求</font>**<font style="color:rgb(51, 51, 51);">：GPT-4V等模型展现多模态潜力，但中文领域缺乏高性能开源方案</font>
+ **<font style="color:rgb(51, 51, 51);">技术定位</font>**<font style="color:rgb(51, 51, 51);">：作为Qwen系列（如Qwen-7B）的多模态扩展，专注于解决高分辨率图像理解、细粒度定位等难点</font>
+ **<font style="color:rgb(51, 51, 51);">开源优势</font>**<font style="color:rgb(51, 51, 51);">：提供中英双语支持，参数量可控（约9.6B），适配消费级GPU</font>

<font style="color:rgb(25, 27, 31);">一般称</font>**<font style="color:#ED740C;">Qwen-VL为multi task learning之后的模型</font>**<font style="color:rgb(25, 27, 31);">，而称</font>**<font style="color:#ED740C;">Qwen-VL-Chat为SFT之后的模型</font>**<font style="color:rgb(25, 27, 31);">。</font>

**paper : **[**https://arxiv.org/pdf/2308.12966**](https://arxiv.org/pdf/2308.12966)

**<font style="color:rgb(25, 27, 31);">参考</font>**<font style="color:rgb(25, 27, 31);">：</font>[如何评价千问发布的Qwen2.5-VL?](https://www.zhihu.com/question/10742671583) [多模态技术梳理：Qwen-VL系列](https://zhuanlan.zhihu.com/p/25267823390)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| 维度 | 创新描述 |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">视觉编码</font>** | <font style="color:rgb(51, 51, 51);">动态高分辨率策略：将图像分割为448x448 patches（最高达1664x1664分辨率）</font> |
| **<font style="color:rgb(51, 51, 51);">训练框架</font>** | <font style="color:rgb(51, 51, 51);">三阶段渐进式训练：视觉编码器预训练 → 多模态对齐 → 指令微调</font> |
| **<font style="color:rgb(51, 51, 51);">跨模态融合</font>** | <font style="color:rgb(51, 51, 51);">轻量级Adapter设计（仅0.1B参数），通过Q-former连接视觉与语言模型</font> |
| **<font style="color:rgb(51, 51, 51);">任务支持</font>** | <font style="color:rgb(51, 51, 51);">支持检测框输出（格式：</font>`<font style="color:rgb(51, 51, 51);"><box>(x1,y1,x2,y2)</box></font>`<font style="color:rgb(51, 51, 51);">）与多轮对话</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| **阶段** | **数据类型** | **规模** | **示例来源** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练</font>** | <font style="color:rgb(51, 51, 51);">图像-文本对</font> | <font style="color:rgb(51, 51, 51);">1.5B</font> | <font style="color:rgb(51, 51, 51);">LAION-COCO, Objects365, OCR数据</font> |
| **<font style="color:rgb(51, 51, 51);">多任务预训练</font>** | <font style="color:rgb(51, 51, 51);">区域标注数据</font> | <font style="color:rgb(51, 51, 51);">60M</font> | <font style="color:rgb(51, 51, 51);">RefCOCO, VQA v2,检测数据集</font> |
| **<font style="color:rgb(51, 51, 51);">微调阶段</font>** | <font style="color:rgb(51, 51, 51);">指令数据</font> | <font style="color:rgb(51, 51, 51);">0.5M</font> | <font style="color:rgb(51, 51, 51);">人工标注、GPT-4生成的多轮对话</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(51, 51, 51);">文本：Qwen-7B</font>
+ <font style="color:rgb(51, 51, 51);">视觉：ViT-bigG</font>
+ <font style="color:rgb(51, 51, 51);">多模态Adaptor(多模态对齐)：</font>
    - <font style="color:rgb(51, 51, 51);">可学习查询向量(</font>**<font style="color:#ED740C;">Q-Former</font>**<font style="color:rgb(51, 51, 51);">)：为缓解长图像特征引起的效率问题，Qwen VL引入了一种</font>**<font style="color:#74B602;">压缩图像特征的视觉语言适配器</font>**<font style="color:rgb(51, 51, 51);">。此适配器包括随机初始化的</font>**<font style="color:#74B602;">单层交叉注意力模块</font>**<font style="color:rgb(51, 51, 51);">。该模块使用一组可训练的向量（embeddings）作为查询向量，来自视觉编码器的图像特征作为交叉注意力操作的关键。该机制将视觉特征序列压缩到</font>**<font style="color:#74B602;">256的固定长度</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">此外，</font>**<font style="color:#74B602;">考虑到位置信息对细粒度图像理解的重要性</font>**<font style="color:rgb(51, 51, 51);">，</font>**<font style="color:#74B602;">2D绝对位置编码整合到交叉注意力机制的查询KV对中</font>**<font style="color:rgb(51, 51, 51);">，以减轻位置的潜在损失压缩过程中的细节。长度为256的压缩图像特征序列随后被馈送到大型语言模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078135089-c01d6207-8a96-47ed-8084-cd2219eaff0b.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742269514251-822b277c-4e60-4834-90e9-2529c75ab06e.png)

**<font style="color:rgb(25, 27, 31);">标准的三阶段训练方法</font>**

1. **<font style="background-color:#D9EAFC;">预训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **数据**：利用大规模、弱标记、网络爬行的图像文本集对。我们努力清理某些模式的数据集。如表2所示，原始数据集总共包含50亿个图像-文本对，经过清理后，剩余14亿个数据，其中77.3%为英文。中文（文本）数据占22.7%

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077353636-eb920e51-03ea-415e-8671-3b6fe736fd14.png)

b. **预训练**：**<font style="color:#74B602;">冻结LLM，只优化了视觉编码器和VL适配器</font>**。输入图像的大小调整为224×224。训练目标是最小化文本标记。最大学习率为2e−4，训练过程使用batch-size30720的图像-文本对，整个预训练的第一阶段持续50000步，大约消耗<font style="color:#74B602;">1.5B的图文对</font>。

2. **<font style="background-color:#D9EAFC;">多任务预训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **数据**：引入高质量和细粒度的图文注释，具有更大输入分辨率的数据。我们对Qwen-VL**<font style="color:#74B602;">同时训练7项任务</font>**。对于文本生成，使用内部收集的语料库来维护。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077714073-c8414b2f-b84c-466f-b520-9b31c45c50c3.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078058838-feca87bb-7b60-40c5-aed6-a612b4341408.png)

    - **训练**：分辨率从224×224提高到448×448，减少了信息量图像下采样造成的损失。此外，我们使用了window attention和global attention。我们**<font style="color:#74B602;">对视觉、LLM、VL投影都进行训练</font>**，训练目标与预训练阶段相同。
3. **<font style="background-color:#D9EAFC;">SFT</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    - **数据：**指令调优数据总计35万。**<font style="color:#74B602;">混合了多模态和纯文本对话训练过程中的数据</font>**，以确保模型在对话能力方面的通用性。指令调优数据总计35万。在此阶段，我们**<font style="color:#74B602;">冻结视觉编码器并优化语言模型和适配器模块</font>**。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078073564-bb09f492-d8d1-45ce-9128-908fe4367251.png)

    - **训练：**通过指令微调来微调Qwen VL预训练模型，以增强其指令跟踪和对话能力，形成了交互式Qwen VL聊天模型。

:::color5
**<font style="color:#601BDE;">5.训练参数</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741077454810-04621823-335f-4f7b-ac3f-c49960310269.png)

:::color5
**<font style="color:#601BDE;">6.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">高分辨率处理能力（比CLIP提升4倍细节）</font>
+ <font style="color:rgb(51, 51, 51);">支持检测框输出（无需额外检测头）</font>
+ <font style="color:rgb(51, 51, 51);">中英双语优化</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">推理速度较慢（处理1024px图像需约5s/RTX3090）</font>
+ <font style="color:rgb(51, 51, 51);">复杂推理能力弱于GPT-4V</font>

:::color5
**<font style="color:#601BDE;">7.应用场景</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

| 场景 | 示例 |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">医学影像</font> | <font style="color:rgb(51, 51, 51);">病理报告生成 + 病灶区域标注</font> |
| <font style="color:rgb(51, 51, 51);">电商</font> | <font style="color:rgb(51, 51, 51);">商品详情页解析（价格、规格提取）</font> |
| <font style="color:rgb(51, 51, 51);">教育</font> | <font style="color:rgb(51, 51, 51);">手写公式识别与解题步骤生成</font> |


:::color5
**<font style="color:#601BDE;">8.改进方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **效率优化**：
    - <font style="color:rgb(51, 51, 51);">动态token压缩（如对非关键区域降采样）</font>
    - <font style="color:rgb(51, 51, 51);">量化部署：使用AWQ技术压缩至4bit</font>
2. **性能提升**：
    - <font style="color:rgb(51, 51, 51);">引入扩散模型提升细粒度生成质量</font>
    - <font style="color:rgb(51, 51, 51);">集成检索增强（RAG）减少幻觉</font>

:::color5
**<font style="color:#601BDE;">9.代码实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image

# 加载模型
model = AutoModelForCausalLM.from_pretrained("qwen-vl-chat", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("qwen-vl-chat")

# 处理输入
image = Image.open("cat.jpg").convert("RGB")
text = "<img>cat.jpg</img> 描述图中的猫的位置，用检测框表示。"

# 生成输出
inputs = tokenizer(text, images=image, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0]))

# 输出示例：
# <box>(253,156,398,290)</box> 图中有一只橘色猫坐在窗台上，面向窗外。

```

## InternVL系列
### InternVL 3.5
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ **<font style="color:rgb(25, 27, 31);">现状挑战：</font>**<font style="color:rgb(25, 27, 31);">当前开源多模态大语言模型（MLLMs）在推理能力、计算效率上与商业模型（如 GPT-5）存在显著差距，且多模态能力增强常伴随计算成本激增。</font>
+ **<font style="color:rgb(25, 27, 31);">研究目标：</font>**<font style="color:rgb(25, 27, 31);">推出 InternVL3.5，通过创新技术解决</font>**<font style="color:#117CEE;">「通用性不足、推理弱、效率低」</font>**<font style="color:rgb(25, 27, 31);">三大痛点，缩小与商业模型的性能差距。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternVL3.5 是上海 AI 实验室推出的开源多模态模型家族，核心目标是提升模型的通用性、推理能力与推理效率。其关键创新包括：</font>[**<font style="color:#ED740C;">Cascade Reinforcement Learning</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=Cascade+Reinforcement+Learning&zhida_source=entity)**<font style="color:#ED740C;">（Cascade RL）、Visual Resolution Router（ViR）、Decoupled Vision-Language Deployment（DvD）</font>**<font style="color:rgb(25, 27, 31);">。模型覆盖 1B 到 241B 参数规模，新增GUI 交互、具身智能、SVG 理解与生成等能力。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[**https://github.com/OpenGVLab/InternVL**](https://github.com/OpenGVLab/InternVL)

**paper：**[**https://arxiv.org/pdf/2508.18265**](https://arxiv.org/pdf/2508.18265)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029427608-75cc8a07-aa05-47ea-ab62-c04d1ef879f5.png)

> 总体架构。InternVL3.5与之前的版本一样采用“ViT-MLP-LLM”范式。在InternVL3.5的基础上，我们进一步介绍了InternVL3.5-Flash，对每个patch，它扩展了额外的视觉分辨率路由器（ViR）动态选择适当的压缩率（例如，1/4或1/16）。与仅从图像宽度角度分割图像块的动态高分辨率不同，我们提出的ViR从语义内容的角度进一步引入了自适应性。
>

:::color5
**<font style="color:#601BDE;">1.关键架构优化 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">动态高分辨率策略：</font>**<font style="color:rgb(25, 27, 31);">延续 InternVL1.5 设计，支持 1:1/1:2/1:3 等预设宽高比，适配不同图像输入。</font>
2. **<font style="color:rgb(25, 27, 31);">ViR 模块（仅 Flash 版）：</font>**<font style="color:rgb(25, 27, 31);">通过「语义 richness 评估」为每个图像 patch 选择压缩率（1/4→256 token，1/16→64 token），减少视觉 token 数量。</font>

:::color5
**<font style="color:#601BDE;">2.级联强化学习（Cascade RL）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029970182-26f70284-4c67-4eb8-b7ad-e0c10324f811.png)

> InternVL3.5的训练食谱。InternVL3.5包括三个培训阶段：（1）native pretraining 用于视觉语言对齐，（2）SFT 以适应下游任务，（3）Cascade RL以提高推理能力。InternVL3.5-Flash是InternVL3.5的高效版本通过一致性训练和路由器训练进一步集成视觉分辨率路由器（ViR）。
>

<font style="color:rgb(25, 27, 31);">Cascade RL 旨在结合离线强化学习（RL）和在线 RL 的优势，解决单一 RL 范式在多模态大语言模型（MLLMs）中面临的效率和稳定性问题。其实现分为两个关键阶段：</font>

1. **<font style="color:rgb(25, 27, 31);">离线阶段（使用 </font>**[**<font style="color:rgb(9, 64, 142);">MPO 算法</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=MPO+%E7%AE%97%E6%B3%95&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：利用 MMPR-v1.2 数据集（包含 200K 样本对）进行训练，计算损失函数为偏好损失（DPO）、质量损失（BCO）和生成损失（LM）的加权和，公式表示为</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029919600-0de007b4-b7ae-4be6-ab0c-5ef768f10e5c.png)

<font style="color:rgb(25, 27, 31);">在此阶段，模型能够快速收敛至一个满意的性能水平，为在线阶段提供高质量的 rollout 数据。</font>

2. **<font style="color:rgb(25, 27, 31);">在线阶段（使用 </font>**[**<font style="color:rgb(9, 64, 142);">GSPO 算法</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=GSPO+%E7%AE%97%E6%B3%95&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">：基于 MMPR-Tiny 数据集（包含 70K 查询，筛选自模型准确率在 0.2-0.8 之间的样本），通过归一化奖励计算优势函数，公式为</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029942337-4a119e16-455f-49bf-970b-3480551e2342.png)

<font style="color:rgb(25, 27, 31);">GSPO 算法无需参考模型的约束，能够有效提升模型的推理上限，并且适用于 dense 和 MoE 两种模型架构。通过 Cascade RL，InternVL3.5 全规模模型的推理性能得到显著提升。例如，InternVL3.5-2B 模型在推理任务中的得分从 SFT 后的 38.5 分提升至 50.7 分，提升幅度达到 + 12.2%，充分展示了该技术在增强模型推理能力方面的有效性。</font>

:::color5
**<font style="color:#601BDE;">3.视觉分辨率路由（ViR）与 视觉一致性训练（</font>**[**<font style="color:#601BDE;">ViCO</font>**](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=ViCO&zhida_source=entity)**<font style="color:#601BDE;">）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">ViR 的核心目标是在不损失模型性能的前提下，减少视觉 token 的数量，从而降低推理成本。为实现这一目标，ViCO 训练过程分为两个阶段：</font>

1. **<font style="color:rgb(25, 27, 31);">一致性训练</font>**<font style="color:rgb(25, 27, 31);">：冻结参考模型（InternVL3.5），通过最小化不同压缩率（1/4 或 1/16）视觉 token 的输出分布差异来进行训练，差异度量使用 KL 散度。此阶段确保模型在不同分辨率下的输出一致性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030121907-d2416523-7bd5-4564-a9d3-0b5d2ec46c50.png)

2. **<font style="color:rgb(25, 27, 31);">路由器训练</font>**<font style="color:rgb(25, 27, 31);">：将 ViR 视为一个二分类器，通过交叉熵损失进行训练。基于压缩前后损失比</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030144855-1dd3f4c4-43ea-4587-b3f5-61e4b7323231.png)

<font style="color:rgb(25, 27, 31);">来标注标签。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030168012-f41047fe-13eb-4f1d-9709-f0f21b24446f.png)<font style="color:rgb(25, 27, 31);">  
</font>

<font style="color:rgb(25, 27, 31);">实验结果表明，集成 ViR 的 InternVL3.5-Flash 系列模型能够减少 50% 的视觉 token，同时在 DocVQA、InfoVQA 等任务上性能保留率达到 99% 以上。例如，8B 模型在 DocVQA 任务中的得分，采用 ViR 前后分别为 91.9 分和 92.3 分，几乎无性能损失，验证了 ViR 技术在提升模型推理效率方面的可行性。</font>

:::color5
**<font style="color:#601BDE;">4.解耦的视觉语言部署（DvD）</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">传统的视觉 - 语言模型部署方式中，视觉编码器（通常具有并行计算特性）与语言模型（自回归计算）串行执行，容易导致资源阻塞，降低推理效率。DvD 技术通过以下方式优化部署架构：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759030220913-d9829c02-7055-4275-8126-c76811445712.png)<font style="color:rgb(25, 27, 31);"></font>

1. **<font style="color:rgb(25, 27, 31);">分离部署</font>**<font style="color:rgb(25, 27, 31);">：将视觉服务器（包含 ViT、MLP 和 ViR 模块）和语言服务器（仅运行 LLM）分离，视觉服务器处理图像并生成 BF16 特征，通过 TCP/RDMA 协议传输至语言服务器。</font>
2. **<font style="color:rgb(25, 27, 31);">流水线优化</font>**<font style="color:rgb(25, 27, 31);">：采用异步并行的方式处理视觉处理、特征传输和语言解码过程，减少处理过程中的 stalls，提高整体推理效率。在实际应用中，单 DvD 技术可实现 1.87-2.01 倍的加速效果，当与 ViR 结合时，加速效果最高可达 4.05 倍。以 38B 模型在 896 分辨率下为例，推理吞吐量从 2.71 req/s 提升至 10.97 req/s，充分证明了 DvD 在提升模型推理效率方面的显著优势。</font>

:::color5
**<font style="color:#601BDE;">5.模型架构设计</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL3.5 延续了 “ViT–MLP–LLM” 的基础范式，并针对不同的应用场景和资源需求，设计了多样化的模型架构，涵盖 dense 和 MoE 两种类型，具体如下：</font>

1. **<font style="color:#117CEE;">Dense 模型系列</font>**
    1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：提供两种选择，分别是适用于轻量级模型的 </font>[<font style="color:rgb(9, 64, 142);">InternViT-300M</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=InternViT-300M&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 和适用于大规模模型的 </font>[<font style="color:rgb(9, 64, 142);">InternViT-6B</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=InternViT-6B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。InternViT-300M 具有较低的计算成本，适合在资源受限的环境中运行；InternViT-6B 则能够处理更复杂的视觉信息，为大型模型提供更强大的视觉特征提取能力。</font>
    2. **<font style="color:rgb(25, 27, 31);">语言模型</font>**<font style="color:rgb(25, 27, 31);">：基于 </font>[<font style="color:rgb(9, 64, 142);">Qwen3</font>](https://zhida.zhihu.com/search?content_id=262281836&content_type=Article&match_order=1&q=Qwen3&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 系列构建，包括 Qwen3-0.6B、Qwen3-1.7B、Qwen3-4B、Qwen3-8B、Qwen3-14B 和 Qwen3-32B 等不同参数规模的模型。这些语言模型在自然语言处理方面具有良好的基础性能，与视觉编码器协同工作，实现多模态信息的融合和处理。</font>
2. **<font style="color:#117CEE;">MoE 模型系列</font>**
    1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：同样采用 InternViT-300M 或 InternViT-6B，根据模型规模和性能需求进行选择。</font>
    2. **<font style="color:rgb(25, 27, 31);">语言模型</font>**<font style="color:rgb(25, 27, 31);">：使用具有混合专家（MoE）架构的模型，如 Qwen3-20B-A4B、Qwen3-30B-A3B 和 Qwen3-235B-A22B 等。MoE 架构通过动态路由机制，能够在不同的输入情况下选择最合适的专家模块进行处理，有效提高模型的表达能力和计算效率，尤其适用于处理大规模、复杂的多模态数据。</font>
3. **<font style="color:#117CEE;">高效变体：InternVL3.5-Flash</font>**

<font style="color:rgb(25, 27, 31);">针对资源受限的场景，InternVL3.5 推出了高效变体 InternVL3.5-Flash。该系列模型在原有架构的基础上集成了 ViR 模块，通过动态调整视觉 token 的分辨率，在减少视觉 token 数量的同时保持模型性能。这种设计使得模型能够在低资源环境下实现高效推理，拓宽了模型的应用范围。</font>

:::color5
**<font style="color:#601BDE;">6.训练流程与数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL3.5 的训练流程经过精心设计，包括预训练、监督微调（SFT）、Cascade RL 和 ViCO（仅针对 Flash 版）等多个阶段，每个阶段都使用特定的数据和目标来逐步提升模型的性能：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1759029970182-26f70284-4c67-4eb8-b7ad-e0c10324f811.png)

> InternVL3.5的训练食谱。InternVL3.5包括三个培训阶段：（1）native pretraining 用于视觉语言对齐，（2）SFT 以适应下游任务，（3）Cascade RL以提高推理能力。InternVL3.5-Flash是InternVL3.5的高效版本通过一致性训练和路由器训练进一步集成视觉分辨率路由器（ViR）。
>

1. **<font style="color:rgb(25, 27, 31);">预训练阶段</font>**<font style="color:rgb(25, 27, 31);">：使用 116M 样本（总计 250B tokens）进行训练，数据包括纯文本语料库以及图像 - 文本对、视频 - 文本对等多模态数据。训练目标是实现视觉 - 语言的基础对齐，通过最小化 next token prediction（NTP）损失，并采用 square averaging 加权策略来平衡不同模态数据的贡献。此外，为增强模型的鲁棒性，训练过程中对图像数据进行随机 JPEG 压缩处理。</font>
2. **<font style="color:rgb(25, 27, 31);">监督微调（SFT）阶段</font>**<font style="color:rgb(25, 27, 31);">：利用 56M 样本（130B tokens）进行微调，数据中加入了更多的推理数据（采用 Thinking 模式）以及新能力相关数据，如 GUI、具身智能、SVG 等方面的数据。此阶段旨在使模型更好地适应各种实际任务，提升模型对用户指令的理解和执行能力。</font>
3. **<font style="color:rgb(25, 27, 31);">Cascade RL 阶段</font>**<font style="color:rgb(25, 27, 31);">：离线阶段使用 MPO 算法，基于 MMPR-v1.2 数据集（200K 样本）进行训练，快速提升模型性能并使其达到稳定状态；在线阶段采用 GSPO 算法，利用 MMPR-Tiny 数据集（70K 查询）进一步优化模型，突破推理性能上限。</font>
4. **<font style="color:rgb(25, 27, 31);">ViCO 阶段（仅 Flash 版）</font>**<font style="color:rgb(25, 27, 31);">：基于 SFT 数据的子集（主要包含 OCR 和 VQA 相关数据）进行训练，通过一致性训练和路由器训练两个步骤，使 ViR 模块能够准确地为每个图像 patch 选择合适的压缩率，同时保持模型在压缩后的性能一致性。  
</font><font style="color:rgb(25, 27, 31);">通过这一系列的训练流程，InternVL3.5 能够充分利用多样化的数据，逐步提升模型在多模态任务中的性能和泛化能力，成为一个功能强大且适应性广泛的多模态模型家族。</font>

:::color5
**<font style="color:#601BDE;">7.总结</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:#117CEE;">关键结论</font>**
    - <font style="color:rgb(25, 27, 31);">推理能力开源领先：Cascade RL 使 InternVL3.5 全规模模型推理性能提升 10-16%，旗舰模型成为开源推理能力最强的 MLLM。</font>
    - <font style="color:rgb(25, 27, 31);">效率与性能兼顾：ViR+DvD 实现 4.05× 推理加速，且性能无损，适配高分辨率、多图像等复杂场景。</font>
    - <font style="color:rgb(25, 27, 31);">通用性覆盖广泛：新增 GUI、具身、SVG 能力，文本任务性能接近商业模型，成为 “全场景适配” 的开源多模态模型。</font>
2. **<font style="color:#117CEE;">未来方向</font>**
    - <font style="color:rgb(25, 27, 31);">进一步优化幻觉抑制能力，减少多模态生成中的事实性错误。</font>
    - <font style="color:rgb(25, 27, 31);">扩展更长的视觉上下文（如超长篇视频理解），提升复杂场景适配性。</font>
    - <font style="color:rgb(25, 27, 31);">深化多语言多模态能力，覆盖更多小语种的跨模态任务。</font>

### InternVL 2.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。研究人员有一些有趣的发现：</font>

1. **<font style="color:rgb(25, 27, 31);">大型视觉编码器的优势</font>**<font style="color:rgb(25, 27, 31);">：大型视觉编码器在扩展多模态大模型时显著减少了对训练数据的依赖。与配备600M视觉编码器的Qwen2-VL-72B相比，InternVL2.5-78B配备了6B的视觉编码器，仅使用1/10的训练token就能实现更好的性能。这大大降低了扩展多模态大模型时的探索成本。</font>
2. **<font style="color:rgb(25, 27, 31);">数据质量的重要性</font>**<font style="color:rgb(25, 27, 31);">：从InternVL 2.0升级到2.5时，数据集规模增加了一倍，但严格的过滤大大提高了数据质量。例如，研究人员仔细排除了异常样本（如重复模式），在</font>[<font style="color:rgb(9, 64, 142);">链式推理</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E9%93%BE%E5%BC%8F%E6%8E%A8%E7%90%86&zhida_source=entity)<font style="color:rgb(25, 27, 31);">任务（如MMMU）和复杂挑战（如OlympiadBench）中取得了显著的改进。值得注意的是，大多数现有的开源多模态大模型在使用链式推理时表现不佳。</font>
3. **<font style="color:rgb(25, 27, 31);">测试时扩展的益处</font>**<font style="color:rgb(25, 27, 31);">：对于困难的多模态问答任务，测试时扩展是有益的。在像MMMU这样的挑战性任务中，InternVL2.5-78B结合链式推理达到了70.1%的准确率，比直接响应高出3.7个百分点。随后，研究人员成功验证了链式推理可以进一步与多数投票结合，带来额外的改进。</font>

:::

:::color3
**简介：**[<font style="color:rgb(9, 64, 142);">InternVL 2.5</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=InternVL+2.5&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，这是一种先进的大规模多模态大模型系列，基于InternVL 2.0的基础架构。InternVL系列的目标是缩小商业闭源模型与开源多模态模型之间的性能差距。在InternVL 2.5中，他们系统地探索了多模态大模型中的各种因素，包括</font>[<font style="color:rgb(9, 64, 142);">视觉编码器</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">、语言模型、</font>[<font style="color:rgb(9, 64, 142);">数据集规模</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%9B%86%E8%A7%84%E6%A8%A1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">和推理时间的变化如何影响模型的整体性能，从而展示了多模态模型中扩展与性能之间的关系。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**https://zhuanlan.zhihu.com/p/12309812997**](https://zhuanlan.zhihu.com/p/12309812997)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539773591-7e23e6f7-d565-4b0f-9cdb-02bf4a7a0e41.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. <font style="color:rgb(25, 27, 31);">加上了</font>**<font style="color:rgb(25, 27, 31);">stage 1.5</font>**<font style="color:rgb(25, 27, 31);">，专门用来训练ViT， 使其对chart等数据表现更好，ViT是和较小的LLm一起训练直接沿用到较大的LLM，节省了训练时间。</font>
2. <font style="color:rgb(25, 27, 31);">随机图像压缩，使模型能够适应图像噪声。</font>
3. <font style="color:rgb(25, 27, 31);">损失函数取了token average和sample average的tradeoff，避免响应长度对最终结果的影响。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练数据**

<font style="color:rgb(25, 27, 31);">为了全面提升模型的性能并增强其处理复杂任务的能力，InternVL 2.5的训练数据集比InternVL 1.5和2.0更广泛且多样化。模型开发期间，专门使用对话格式的指令数据。在这一阶段，由于只有MLP或MLP和ViT的参数是可训练的，因此会</font>**<font style="color:rgb(25, 27, 31);">结合高质量和低质量的数据。</font>**<font style="color:rgb(25, 27, 31);">目标是通过接触多样的领域数据来丰富模型的世界知识，从而提高其泛化能力。训练语料库涵盖了</font>**<font style="color:#74B602;">字幕生成、通用问答、数学、图表、OCR、知识、定位、文档、对话、医疗和GUI任务等领域。</font>**

2. **<font style="color:rgb(25, 27, 31);">微调数据</font>**

<font style="color:rgb(25, 27, 31);">从InternVL 1.5到2.0再到2.5，数据集在规模、质量和多样性上进行了迭代改进。数据规模方面，样本数量从InternVL 1.5的510万增长到InternVL 2.0的730万，并在InternVL 2.5中进一步翻倍至</font>**<font style="color:#74B602;">1630万</font>**<font style="color:rgb(25, 27, 31);">。在多样性方面，训练数据涵盖多个领域，包括</font>**<font style="color:#74B602;">通用问答、图表、文档、OCR、科学、医疗、GUI、代码、数学等，同时覆盖多种模态，如单图像、多图像、视频和文本。</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 2.5中，</font>**<font style="color:#74B602;">单图像数据占据了45.92%的标记，多图像数据占9.37%，视频数据贡献了39.79%，纯文本数据占4.92%</font>**<font style="color:rgb(25, 27, 31);">。与早期版本相比，多图像和视频数据的增加最为显著，增强了InternVL 2.5对多图像和长视频的理解能力。质量提升通过统一对话模板、使用语言模型评分和精炼数据、去除重复模式、应用启发式规则过滤低质量样本，以及将短响应重写为高质量和更长的交互来实现。这确保了模型训练的稳健数据集。</font>

3. **数据处理pipeline**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720896544-874e4e03-d4d1-4892-b359-9c4e86630891.png)

<font style="color:rgb(25, 27, 31);">在模型开发过程中，观察到</font>**<font style="color:#74B602;">LLM对数据噪声的敏感性显著高于视觉编码器</font>**<font style="color:rgb(25, 27, 31);">。即使是少量异常样本（例如，离群值或重复数据，仅数千个）也会在推理期间导致模型行为异常。</font>

<font style="color:rgb(25, 27, 31);">在这些异常中，</font>**<font style="color:#74B602;">重复生成</font>**<font style="color:rgb(25, 27, 31);">被识别为最具破坏性的问题之一。在许多开源或合成数据集中，仅仅数千个重复样本就会导致模型陷入重复循环，尤其是在长篇输出或CoT推理任务中。这种现象削弱了测试时缩放策略的有效性。为应对这一挑战并支持未来研究，我们设计了一种高效的数据过滤管道，以去除低质量样本，从而最大限度地减少重复生成的风险。</font>

**<font style="color:rgb(25, 27, 31);">数据过滤pipeline</font>**<font style="color:rgb(25, 27, 31);">：由两个模块组成。对于纯文本数据，实施了三种关键策略：</font>

1. **<font style="color:rgb(25, 27, 31);">基于LLM的质量评分</font>**<font style="color:rgb(25, 27, 31);">：首先将数据集分类为不同领域，低于指定阈值的样本被移除以确保数据质量。</font>
2. **<font style="color:rgb(25, 27, 31);">重复检测</font>**<font style="color:rgb(25, 27, 31);">：使用LLM结合特定提示识别重复样本。这些样本经过人工审查，低于阈值的样本被移除以保持数据质量。</font>
3. **<font style="color:rgb(25, 27, 31);">启发式规则过滤</font>**<font style="color:rgb(25, 27, 31);">：应用特定规则，如过滤掉异常长度的句子、过长的零序列、过多重复行的文本等，以识别数据中的异常。尽管这种方法可能偶尔产生误报，但它提高了异常样本的检测率。所有标记样本在最终移除前都经过人工审查。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(25, 27, 31);">InternVL 2.5 延续了其前身 InternVL 1.5 和 InternVL 2.0 的模型架构，采用了广泛应用于多模态大语言模型研究中的</font>**<font style="color:#74B602;">“ViT-MLP-LLM”范式</font>**<font style="color:rgb(25, 27, 31);">。</font>

1. **<font style="color:rgb(25, 27, 31);">视觉编码器</font>**

<font style="color:rgb(25, 27, 31);">InternVL 使用 InternViT 作为视觉编码器，当前有两种不同的模型尺寸：InternViT-6B 和 InternViT-300M。</font>

+ **<font style="color:rgb(25, 27, 31);">InternViT-6B</font>**<font style="color:rgb(25, 27, 31);">：最初在 CVPR 论文中引入，采用了基础 ViT 架构，进行了少量调整，如引入了 </font>**<font style="color:#74B602;">QK-Norm 和 RMSNorm</font>**<font style="color:rgb(25, 27, 31);">。该模型有 5.9B 参数，48 层，隐藏层大小为 3200，25 个头，并使用对比损失进行训练。为了不断优化其权重，采用了增量预训练策略，</font>**<font style="color:#74B602;">通过 MLP 投影器将 InternViT-6B 连接到语言模型</font>**<font style="color:rgb(25, 27, 31);">，并使用下一个标记预测损失进行联合训练，以增强其视觉特征提取能力。在后续版本中，采用了动态分辨率训练来提高高分辨率处理能力。</font>
+ **<font style="color:rgb(25, 27, 31);">InternViT-300M</font>**<font style="color:rgb(25, 27, 31);">：这是一个蒸馏变体，使用余弦蒸馏损失，包含 0.3B 参数，24 层，隐藏层大小为 1024，16 个注意力头。与 6B 版本不同，0.3B 版本使用标准 LayerNorm，而不是 QK-Norm。经过蒸馏后，该模型与语言模型集成，并通过动态高分辨率和 </font>[<font style="color:rgb(9, 64, 142);">NTP 损失</font>](https://zhida.zhihu.com/search?content_id=251484927&content_type=Article&match_order=1&q=NTP+%E6%8D%9F%E5%A4%B1&zhida_source=entity)<font style="color:rgb(25, 27, 31);">训练视觉编码器。</font>
2. **<font style="color:rgb(25, 27, 31);">大语言模型</font>**

<font style="color:rgb(25, 27, 31);">InternVL 系列中使用的语言模型包括 InternLM 2、Qwen 2、Phi 3、Yi 和 Llama 3。为了实现更好的性能，InternVL 2.5 系列全面升级了语言模型骨干，采用了最新的先进模型，如</font>**<font style="color:#74B602;"> InternLM 2.5 和 Qwen 2.5</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742720683356-162dbf4f-db1e-4cb8-bc02-8ac81eced6f5.png)

1. **<font style="color:rgb(25, 27, 31);">阶段1：MLP预热</font>**

<font style="color:rgb(25, 27, 31);">在这一阶段，首先对</font>**<font style="color:#74B602;">MLP投影器进行预热训练</font>**<font style="color:rgb(25, 27, 31);">。MLP投影器是视觉和语言表示之间的初始桥梁。在此阶段，仅训练MLP投影器，而视觉编码器（InternViT）和语言模型保持冻结状态。尽管这种动态高分辨率训练策略增加了训练成本，但它有助于实现最佳性能。在这一阶段，使用预训练数据混合，并采用NTP损失进行优化。应用较高的学习率以加速收敛，使MLP能够快速适应LLM的输入空间，并建立稳健的跨模态对齐。MLP预热阶段确保模型在解锁后续阶段的可训练组件之前，能够良好地处理多模态任务，从而提高训练稳定性。</font>

1. **<font style="color:rgb(25, 27, 31);">阶段1.5：ViT增量学习（可选）</font>**

<font style="color:rgb(25, 27, 31);">阶段1.5为视觉编码器引入增量学习。在这一阶段，</font>**<font style="color:#74B602;">视觉编码器和MLP投影器均可训练</font>**<font style="color:rgb(25, 27, 31);">，训练使用与阶段1相同的预训练数据混合和NTP损失。此阶段的目标是增强视觉编码器提取视觉特征的能力，使其能够捕捉更全面的信息，</font>**<font style="color:rgb(25, 27, 31);">尤其是针对那些在大规模网络数据集中相对稀缺的领域，如多语言OCR数据和数学图表等</font>**<font style="color:rgb(25, 27, 31);">。使用较低的学习率以防止灾难性遗忘，确保编码器不会丧失先前学到的能力。</font>**<font style="color:rgb(25, 27, 31);">视觉编码器一旦训练完成，可以与不同的LLM重复使用，无需重新训练</font>**<font style="color:rgb(25, 27, 31);">，这使得阶段1.5成为可选。这在编码器已经为某些特定任务优化时尤为有利，允许其与各种大小的LLM集成，而无需显著增加成本。</font>

1. **<font style="color:rgb(25, 27, 31);">阶段2：全模型指令微调</font>**

<font style="color:rgb(25, 27, 31);">在最终阶段，整个模型（包括ViT、MLP和LLM）在高质量的多模态指令数据集上进行训练。此时，数据质量尤为重要，因为负责生成最终用户输出的LLM现在是可训练的。</font>**<font style="color:rgb(25, 27, 31);">即使少量的噪声数据（如几千个样本）也可能导致模型行为异常，如输出重复或产生特定错误结果</font>**<font style="color:rgb(25, 27, 31);">。为减轻LLM的退化，在这一阶段实施严格的数据质量控制。此外，此阶段的训练超参数保持简单，对整个模型应用统一的学习率，而不是对不同组件使用不同的学习率。完成此阶段后，InternVL 2.5的完整训练过程即告结束。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

<font style="color:rgb(25, 27, 31);">基本上在各个benchmark上，8B就能和GPT-4o的效果媲美。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721084444-6f390d10-507d-498a-84b9-d714dfa0dad4.png)

<font style="color:rgb(25, 27, 31);">在真实场景的数据集上效果也不错，在我们的</font>[MME-RealWorld](https://link.zhihu.com/?target=https%3A//mme-realworld.github.io/home_page.html)<font style="color:rgb(25, 27, 31);">中8B超过了Qwen2-VL与LLaVA-OV同等量级的模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721124147-e89b9552-ec46-49dc-b003-34fe9fb78b9f.png)

<font style="color:rgb(25, 27, 31);">COT对reasoning的影响：新一版的26B模型在CoT的效果上更好。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742721139524-f54f189f-93b4-453a-8080-d62a1fac0927.png)

### InternVL 2<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternVL2，强大的开源多模态大型语言模型（MLLM）。</font>**<font style="color:rgb(25, 27, 31);">InternVL2家族包括从适合边缘设备的2B模型到更为强大的108B模型。</font>**<font style="color:rgb(25, 27, 31);">随着更大规模语言模型的引入，InternVL2-Pro展示了出色的多模态理解能力，在各种基准测试中与商业闭源模型的性能相匹配。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539773591-7e23e6f7-d565-4b0f-9cdb-02bf4a7a0e41.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ **<font style="color:rgb(25, 27, 31);">逐步采用更大规模的语言模型</font>**<font style="color:rgb(25, 27, 31);">：我们引入了一种逐步对齐训练策略，产生了第一个与大型语言模型原生对齐的视觉基础模型。</font>**<font style="color:rgb(25, 27, 31);">通过采用逐步训练策略，模型从小规模逐步扩展到大规模，同时数据从粗糙逐步精细化，我们以相对较低的成本完成了大规模模型的训练</font>**<font style="color:rgb(25, 27, 31);">。这种方法在资源有限的情况下展现了出色的性能。</font>
+ **<font style="color:rgb(25, 27, 31);">多模态输入</font>**<font style="color:rgb(25, 27, 31);">：我们的模型通过一组参数</font>**<font style="color:rgb(25, 27, 31);">支持多种输入模态</font>**<font style="color:rgb(25, 27, 31);">，包括文本、图像、视频和医疗数据。</font>
+ **<font style="color:rgb(25, 27, 31);">多任务输出</font>**<font style="color:rgb(25, 27, 31);">：得益于我们最近的工作</font>[<font style="color:rgb(9, 64, 142);">VisionLLMv2</font>](https://zhida.zhihu.com/search?content_id=244561702&content_type=Article&match_order=1&q=VisionLLMv2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，我们的模型</font>**<font style="color:rgb(25, 27, 31);">支持多种输出格式，如图像、边界框和掩码，展现了广泛的通用性</font>**<font style="color:rgb(25, 27, 31);">。通过将MLLM与多个下游任务解码器连接，InternVL2可以泛化到数百个视觉-语言任务，同时达到与专家模型相当的性能。</font>

:::color5
**<font style="color:#601BDE;">2.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">阶段1：预训练</font>**

<font style="color:rgb(25, 27, 31);">在InternVL 1.5中使用的预训练数据集扩展了从多种来源收集的数据。</font>**<font style="color:rgb(25, 27, 31);">这些数据集覆盖了多个任务，包括标题生成、视觉问答、检测、定位和OCR。</font>**<font style="color:rgb(25, 27, 31);">OCR数据集是使用PaddleOCR对来自Wukong的中文图像和来自LaionCOCO的英文图像进行OCR构建的，并经过人工验证。此外，我们还爬取了来自uworld、kaptest、testbank、aga和sat的考试数据，并进行了人工解析。还利用了来自OmniCorpus的交错数据。</font>

2. **<font style="color:rgb(25, 27, 31);">阶段2：微调</font>**

<font style="color:rgb(25, 27, 31);">基于InternVL 1.5中使用的500万高质量双语数据集构建了训练数据。具体来说，我们包括了诸如EgoTaskQA、Mementos、STAR、NTU RGB+D、VideoChat2IT和LSMDC-QA这样的</font>**<font style="color:rgb(25, 27, 31);">视频数据</font>**<font style="color:rgb(25, 27, 31);">，以及Medical-Diff-VQA、Pathology-VQA、PMC-CaseReport、PMC-VQA、Slake和VQA-RAD这样的</font>**<font style="color:rgb(25, 27, 31);">医疗数据</font>**<font style="color:rgb(25, 27, 31);">。我们还包括了SROIE、FUNSD和POIE，以</font>**<font style="color:rgb(25, 27, 31);">进一步增强模型识别手写字体的能力</font>**<font style="color:rgb(25, 27, 31);">。此外，我们排除了来自ShareGPT-4V的所有数据，并用来自ShareGPT-4o的数据替换。</font>

:::color5
**<font style="color:#601BDE;">3.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742539863216-dac72ce1-0dc9-4067-a9be-f4f195bbd92c.png)

### InternVL 1.5<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);"> InternVL 1.5，一个</font>**<font style="color:#ED740C;">旨在缩小与商业多模态模型能力差距</font>**<font style="color:rgb(25, 27, 31);">的开源多模态大型语言模型（MLLM）。该模型通过三个主要改进来增强其性能：</font>**<font style="color:#ED740C;">强大的视觉编码器、动态高分辨率处理和高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">。这些改进使得 InternVL 1.5 在视觉理解和语言处理方面表现出色，特别是在处理高分辨率图像和多模态任务时。</font>

**paper：**[**https://arxiv.org/pdf/2404.16821**](https://arxiv.org/pdf/2404.16821)<font style="color:#D22D8D;">（by草莓师姐）</font>

**参考：**[**书生·万象多模态大模型（InternVL）系列**](https://zhuanlan.zhihu.com/p/703940563)**  **[**InternVL1.5 解读**](https://zhuanlan.zhihu.com/p/703135536)** **[**Intern-VL 动态分辨率代码**](https://zhuanlan.zhihu.com/p/14202602450)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537624418-3e85701e-2b23-47d2-a1cf-d42533b6b26c.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">强视觉编码器</font>**<font style="color:rgb(25, 27, 31);">：我们为大规模视觉基础模型</font>[<font style="color:rgb(9, 64, 142);">InternViT-6B</font>](https://zhida.zhihu.com/search?content_id=244382861&content_type=Article&match_order=1&q=InternViT-6B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">探索了一种持续学习策略，提高了其视觉理解能力，并使其可以在不同的大语言模型中迁移。</font>
2. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">动态高分辨率</font>**<font style="color:rgb(25, 27, 31);">：根据输入图像的长宽比和分辨率，将图像划分为1到40个448×448像素的图块，最高支持4K分辨率输入。</font>
3. **<font style="color:rgb(25, 27, 31);">高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">：我们精心收集了</font>**<font style="color:#74B602;">高质量的双语数据集</font>**<font style="color:rgb(25, 27, 31);">，涵盖常见场景、文档图像，并用英文和中文问答对对其进行注释，显着提高了 OCR 和中文相关任务的性能。</font>

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **预训练数据**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537788003-9c17b288-6ec0-4829-bb57-9522be155104.png)

2. **微调数据**<font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537796140-04924915-98c4-4f7b-983d-af7ee2e4f020.png)

3. **语料翻译pipeline（英译中）**<font style="color:#D22D8D;">（by草莓师姐）</font>

```python
System：
你是一名精通英语和{语言}的翻译。你的任务是将以下英文文本翻译成{语言}，注重自然流畅的结果，避免“翻译”。请考虑以下几点：
1.保留英文专有名词、品牌和地名。
2.保留英文技术术语或行话，但必要时用{语言}解释。
3.使用{语言}习语表达英语习语或谚语，以确保文化相关性。
4.确保引用或直接讲话在{语言}中听起来很自然，保持原作的基调。
5.对于缩略语，请提供{语言}的完整形式，并附上括号内为英文首字母缩写。
User：
翻译文本：{Text}
Assistant：
{翻译结果}
```

:::color5
**<font style="color:#601BDE;">2.动态分辨率  </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(25, 27, 31);">动态分辨率：</font>**<font style="color:rgb(25, 27, 31);">训练图像的分辨率从固定的 448×448 扩展到动态 448×448，其中patch大小为 448×448，patch数量范围为 1 到 12。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537741384-75721322-7fa4-4bca-97ce-e49a14ccff86.png)

1. **Pixel Shuffle**<font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">为了提高高分辨率下的可扩展性，我们简单地采用了</font>[**<font style="color:#74B602;">Pixel shuffle</font>**](https://zhida.zhihu.com/search?content_id=244382861&content_type=Article&match_order=1&q=Pixel+shuffle&zhida_source=entity)**<font style="color:#74B602;">操作，将视觉标记的数量减少到原来的四分之一</font>**<font style="color:rgb(25, 27, 31);">。因此，在我们的模型中，一幅 448×448 的图像由 256 个视觉标记表示。</font>

```python
def pixel_shuffle(self, x, scale_factor=0.5):
    n, w, h, c = x.size()
    # N, W, H, C --> N, W, H * scale, C // scale
    x = x.view(n, w, int(h * scale_factor), int(c / scale_factor))
    # N, W, H * scale, C // scale --> N, H * scale, W, C // scale
    x = x.permute(0, 2, 1, 3).contiguous()
    # N, H * scale, W, C // scale --> N, H * scale, W * scale, C // (scale ** 2)
    x = x.view(n, int(h * scale_factor), int(w * scale_factor),
               int(c / (scale_factor * scale_factor)))
    if self.ps_version == 'v1':
        warnings.warn("In ps_version 'v1', the height and width have not been swapped back, "
                      'which results in a transposed image.')
    else:
        x = x.permute(0, 2, 1, 3).contiguous()
    return x
```

2. **<font style="color:rgb(25, 27, 31);">动态宽高比匹配</font>**<font style="color:rgb(25, 27, 31);">：为了在处理过程中保持自然的宽高比，我们从一组预定义的宽高比中动态匹配最佳的宽高比。 由于计算资源有限，我们在训练期间</font>**<font style="color:#74B602;">最多允许 12 个patch</font>**<font style="color:rgb(25, 27, 31);">。 因此，该集合包括由 1 到 12 个patch形成的</font>**<font style="color:#74B602;">所有 35 种可能的宽高比组合，例如 {1:1、1:2、2:1、3:1、…、2:6}</font>**<font style="color:rgb(25, 27, 31);">。 在匹配过程中，对于每个输入图像，我们计算其纵横比，并通过</font>**<font style="color:#74B602;">测量绝对差将其与 35 个预定义的纵横比进行比较，选择最优宽高比</font>**<font style="color:rgb(25, 27, 31);">。 如果多个预定义的宽高比匹配(例如、1:1和2:2），我们会优先考虑不超过输入图像面积两倍的宽高比，从而防止低分辨率图像过度放大。</font><font style="color:#D22D8D;">（by草莓师姐）</font>
3. **<font style="color:rgb(25, 27, 31);">图像resize</font>**<font style="color:rgb(25, 27, 31);">：一旦确定了适当的宽高比，图像的大小就会调整为相应的分辨率。 </font>**<font style="color:#74B602;">例如，800×1300 图像将调整为 896×1344</font>**<font style="color:rgb(25, 27, 31);">。 </font>
4. **<font style="color:rgb(25, 27, 31);">图像patch</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">调整大小的图像被分成 448×448 像素的图块</font>**<font style="color:rgb(25, 27, 31);">。 除了图块之外，</font>**<font style="color:#74B602;">我们还包含整个图像的缩略图以捕获全局上下文。 该缩略图缩小至 448×448</font>**<font style="color:rgb(25, 27, 31);">，帮助模型理解整个场景。</font>

```python
def dynamic_preprocess(image, min_num=1, max_num=6, image_size=448, use_thumbnail=False):
    # 获取原始图像尺寸和计算宽高比 
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # 生成目标宽高比集合：根据给定的最小值 (min_num) 和最大值 (max_num)，生成所有可能的目标宽高比组合 (i, j)，
    # 其中 i * j 在 [min_num, max_num] 范围内
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1) for j in range(1, n + 1) if
        i * j <= max_num and i * j >= min_num)
    
    # 对这些宽高比组合按面积排序，即按 i * j 排序
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # 找到最接近原始宽高比的目标宽高比，这里调用了辅助函数 find_closest_aspect_ratio
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)

    # 计算目标图像的宽度和高度，根据目标宽高比和ViT的原生输入分辨率 (image_size：448) ，
    # 计算目标图像的宽度 (target_width) 和高度 (target_height），以及切图后的子图（448*448）数量
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # 根据计算结果resize
    resized_img = image.resize((target_width, target_height))
    # 将调整后的图像按照目标宽高比分割成多个小块，并存储在列表
    processed_images = []
    # 与Intern-VL不同的是，我的模型还需要动态分辨率模块输出每个子图的相对位置编号
    pos = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
        # 子图所在相对位置
        pos.append(i // (target_width // image_size), i % (target_width // image_size))
    # 检查子图数量是否正确
    assert len(processed_images) == blocks

    # 如果设置了 use_thumbnail 为 True 并且分割后的小块数量不是 1，则将原始图像调整为ViT原生输入大小的缩略图并添加到最后一个小块后面。
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images, pos
```

```python
def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        # 比较宽高比：将输入图像的宽高比与预定义的宽高比进行比较。比较的标准是计算绝对差异，
        # 即找到最接近输入图像宽高比的预定义宽高比
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        # 如果有多个预定义的宽高比与输入图像的宽高比相匹配（例如，1:1 和 2:2），系统会优先选择一个宽高比，
        # 该比率不会导致图像面积扩大超过输入图像面积的两倍。这是为了避免对低分辨率图像进行过度放大。
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    # print(f'width: {width}, height: {height}, best_ratio: {best_ratio}')
    return best_ratio
```

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">InternVL 1.5采用了类似于流行MLLMs的</font>**<font style="color:#74B602;">ViT-MLP-LLM</font>**<font style="color:rgb(25, 27, 31);">架构，通过MLP投影器将预训练的InternViT-6B与InternLM2-20B结合。在这里，我们采用了一个简单的pixel shuffle方法，将视觉tokens的数量减少到四分之一。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537624418-3e85701e-2b23-47d2-a1cf-d42533b6b26c.png)

:::color5
**<font style="color:#601BDE;">4.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

InternVL 1.5与专有商业模型的比较。这些基准测试的结果显示，InternVL 1.5达到了与领先的专有模型相当的性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742538206069-82aed1dd-3c98-4be1-b422-7f38c5848c1c.png)



### InternVL<font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">论文标题：《InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks》</font>

<font style="color:rgb(25, 27, 31);">比较不同视觉和视觉-语言基础模型的差异。如下图所示：</font>

+ <font style="color:rgb(25, 27, 31);">（a）表示传统的视觉基础模型，例如在分类任务上预训练的ResNet[57]。</font>
+ <font style="color:rgb(25, 27, 31);">（b）代表视觉-语言基础模型，例如在图像-文本对上预训练的</font>[<font style="color:rgb(9, 64, 142);">CLIP</font>](https://zhida.zhihu.com/search?content_id=244561702&content_type=Article&match_order=1&q=CLIP&zhida_source=entity)<font style="color:rgb(25, 27, 31);">[117]。</font>
+ <font style="color:rgb(25, 27, 31);">（c）是提出的InternVL，它展示了一种将大规模视觉基础模型（即InternViT-6B）与大型语言模型对齐的可行方法，并且对于对比和生成任务都具有多功能性。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529081885-f82fc2fc-32f3-467b-b11e-9549bb8126a8.png)

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">该模型由南京大学、OpenGVLab、上海人工智能实验室等机构的研究人员共同开发。</font>**<font style="color:#ED740C;">InternVL 模型将视觉编码器扩展到 60 亿参数(6B)，并逐步与大型语言模型（LLM）对齐，使用来自各种来源的 web 规模的图像文本数据进行训练。该模型在 32 个通用视觉语言基准上取得了 state-of-the-art 的性能</font>**<font style="color:rgb(25, 27, 31);">，包括图像级别或像素级别识别、zero-shot图像/视频分类、zero-shot图像/视频-文本检索以及多模态对话系统。</font>

**paper：**[**https://arxiv.org/pdf/2312.14238**](https://arxiv.org/pdf/2312.14238)

**参考：**[**https://zhuanlan.zhihu.com/p/703940563**](https://zhuanlan.zhihu.com/p/703940563)<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529165282-1dd01cee-99c1-413c-adee-cd756c084ceb.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

+ <font style="color:rgb(25, 27, 31);">一是</font>**<font style="color:rgb(25, 27, 31);">参数平衡的视觉和语言组件</font>**<font style="color:rgb(25, 27, 31);">，包括一个 60 亿参数的视觉编码器</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">InternViT-6B</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和一个 80 亿参数的语言中间件</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">QLLaMA</font>**<font style="color:rgb(25, 27, 31);">；</font>
+ <font style="color:rgb(25, 27, 31);">二是</font>**<font style="color:rgb(25, 27, 31);">保持一致的表示</font>**<font style="color:rgb(25, 27, 31);">，通过使用预训练的多语言 LLaMA 来初始化中间件，并使视觉编码器与之对齐；</font>
+ <font style="color:rgb(25, 27, 31);">三是</font>**<font style="color:rgb(25, 27, 31);">采用渐进式图像文本对齐策略</font>**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:#74B602;">通过 contrastive 和 generative 学习阶段</font>**<font style="color:rgb(25, 27, 31);">，有效地利用了 web 规模的嘈杂图像文本数据。</font>

:::color5
**<font style="color:#601BDE;">2.训练方法：三阶段渐进训练</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529165282-1dd01cee-99c1-413c-adee-cd756c084ceb.png)

**<font style="color:#601BDE;">三个渐进阶段</font>**，包括**<font style="color:#74B602;">视觉-语言对比训练、视觉-语言生成训练和监督式微调</font>**。这些阶段有效地利用了来自不同来源的公开数据，从网络上嘈杂的图像-文本对到高质量的字幕、VQA和多模态对话数据集。

1. **<font style="color:rgb(25, 27, 31);">第一阶段，视觉-语言对比训练</font>**
    1. **<font style="color:rgb(25, 27, 31);">目的：</font>**<font style="color:rgb(25, 27, 31);">在Web规模的噪声图像-文本对上进行对比学习，以对齐InternViT-6B与多语言LLaMA-7B </font>
    2. **<font style="color:rgb(25, 27, 31);">数据：</font>**<font style="color:rgb(25, 27, 31);">LAION-en 、LAION-multi 、LAION-COCO、COYO [14]、Wukong等。</font>
    3. **<font style="color:rgb(25, 27, 31);">数据处理</font>**<font style="color:rgb(25, 27, 31);">：我们使用这些数据集的组合，</font>**<font style="color:#74B602;">并过滤掉一些极低质量的数据</font>**<font style="color:rgb(25, 27, 31);">来训练我们的模型。原始数据集包含60.3亿图像-文本对，清洗后剩下49.8亿。</font>
    4. **<font style="color:rgb(25, 27, 31);">训练方法（clip）</font>**<font style="color:rgb(25, 27, 31);">：图文对比学习</font><font style="color:#D22D8D;">（by草莓师姐）</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742529423737-9cb13306-e433-43d6-9400-8f03cdfb5b4b.png)

2. **<font style="color:rgb(25, 27, 31);">第二阶段，视觉-语言生成训练</font>**<font style="color:rgb(25, 27, 31);">。</font><font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **<font style="color:rgb(25, 27, 31);">目的</font>**<font style="color:rgb(25, 27, 31);">：保持InternViT-6B和QLLaMA冻结，训练cross attention 和 learnable queries。这使得</font>**<font style="color:#74B602;">查询能够提取强大的视觉表示，并进一步与大型语言模型（LLMs）对齐特征空间</font>**<font style="color:rgb(25, 27, 31);">，这得益于有效的训练目标和我们大规模、基于LLM初始化的QLLaMA的利用。</font>
    2. **<font style="color:rgb(25, 27, 31);">数据</font>**<font style="color:rgb(25, 27, 31);">：我们进一步过滤掉了低质量标题的数据，</font>**<font style="color:rgb(25, 27, 31);">从第一阶段的49.8亿减少到10.3亿</font>**<font style="color:rgb(25, 27, 31);">。</font>
    3. **<font style="color:rgb(25, 27, 31);">训练方法（blip2）：</font>**<font style="color:rgb(25, 27, 31);">遵循BLIP-2 的损失函数，这一阶段的损失计算为三个组件的总和：图像-文本对比（ITC）损失、图像-文本匹配（ITM）损失和基于图像的文本生成（ITG）损失。</font>
3. **<font style="color:rgb(25, 27, 31);">监督式微调</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>
    1. **<font style="color:rgb(25, 27, 31);">目的</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:rgb(25, 27, 31);">通过仅训练MLP层或同时训练MLP层和QLLaMA来实现稳健的性能。</font>**<font style="color:rgb(25, 27, 31);">这种方法不仅加快了SFT过程，而且还保持了LLMs的原始语言能力。</font>
    2. **<font style="color:rgb(25, 27, 31);">数据</font>**<font style="color:rgb(25, 27, 31);">：收集了广泛的高质量指令数据，</font>**<font style="color:rgb(25, 27, 31);">总共约400万个样本</font>**
    3. **<font style="color:rgb(25, 27, 31);">训练方法：</font>**<font style="color:rgb(25, 27, 31);">通过一个多层感知器（MLP）层将其与现成的LLM解码器（例如Vicuna [184]或InternLM [135]）连接起来，并进行监督式微调（SFT）  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537218718-5d8acb99-62da-444d-ba2f-7fe4182d47f9.png)

:::color5
**<font style="color:#601BDE;">3.评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

零样本图像-文本检索性能的比较。我们使用Flickr30K和COC评估了英语的检索能力，以及使用Flickr30K-C和COCO-C评估了中文的检索能力。†BLIP-在COCO上进行了微调，并零样本转移到Flickr30K上，这有助于提高Flickr30K上的零样本性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742537365482-b710ac9a-eafd-485d-9b78-36973a424cb1.png)



## **CogVLM2**
项目地址：[https://github.com/THUDM/CogVLM2](https://github.com/THUDM/CogVLM2)

<font style="color:rgb(51, 51, 51);">CogVLM2 继承并优化了上一代模型的经典架构，采用了一个拥有50亿参数的强大视觉编码器，并创新性地在大语言模型中整合了一个70亿参数的视觉专家模块。这一模块通过独特的参数设置，精细地建模了视觉与语言序列的交互，确保了在增强视觉理解能力的同时，不会削弱模型在语言处理上的原有优势。这种深度融合的策略，使得视觉模态与语言模态能够更加紧密地结合。与上一代的 CogVLM 模型相比，CogVLM2 系列模型具有以下改进：</font>

+ <font style="color:rgb(51, 51, 51);">在不损失任何通用能力的前提下，在许多关键指标上有了显著提升，如在 OCRbench 基准上性能提升32%，在TextVQA基准上性能提升21.9%，且模型具备了较强的文档图像理解能力（DocVQA）等；</font>
+ <font style="color:rgb(51, 51, 51);">支持 8K 文本长度；</font>
+ <font style="color:rgb(51, 51, 51);">支持高达 1344 * 1344 的图像分辨率；</font>
+ <font style="color:rgb(51, 51, 51);">提供支持中英文双语的开源模型版本。</font>

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472157254-938b8de6-ac1d-4994-b9d1-3594b288ae74.webp)

## **MiniCPM-V**
项目地址：[https://github.com/OpenBMB/MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V)

<font style="color:rgb(51, 51, 51);">MiniCPM-V 2.6 是由面壁智能推出的一款端侧 AI 多模态模型。它在保持较小参数规模的同时，展现出了强大的多模态处理能力，为端侧设备上的人工智能应用提供了新的可能性。</font>

**<font style="color:rgb(51, 51, 51);">主要特点:</font>**

+ <font style="color:rgb(51, 51, 51);">多图理解与上下文学习：MiniCPM-V 2.6 能够支持多图对话与推理。在 Mantis-Eval、BLINK、Mathverse mv 以及 Sciverse mv 等主流多图评测基准中取得了顶尖水平，并且展现出了极为出色的上下文学习能力。</font>
+ <font style="color:rgb(51, 51, 51);">强大的 OCR 能力：MiniCPM-V 2.6 能够处理任意长宽比的图像，像素数可达 180 万（例如 1344x1344）。在 OCRBench 上，它取得了最佳成绩，超越了 GPT-4o、GPT-4V 以及 Gemini 1.5 Pro 等商用闭源模型。</font>
+ <font style="color:rgb(51, 51, 51);">效率卓越：除了对个人用户极为友好的模型大小之外，MiniCPM-V 2.6 还展现出了最为先进的视觉 token 密度（即每个视觉 token 编码的像素数量）。它仅需 640 个 token 即可处理 180 万像素的图像，比大多数模型少 75%。这一特性极大地优化了模型的推理速度、首 token 延迟、内存占用以及功耗。因此，MiniCPM-V 2.6 能够在 iPad 等终端设备上支持高效的实时视频理解。</font>
+ <font style="color:rgb(51, 51, 51);">使用便捷：MiniCPM-V 2.6 可以通过多种方式轻松加以使用：(1) llama.cpp 和 ollama 支持在本地设备上进行高效的 CPU 推理；(2) int4 和 GGUF 格式的量化模型，拥有 16 种尺寸；(3) vLLM 支持高吞吐量和内存高效的推理；(4) 针对新领域和任务进行微调；(5) 使用 Gradio 快速设置本地 WebUI 演示；(6) 通过在线 demo 即可亲身体验。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472159405-d84fc67d-69fe-4050-8179-9c393802a3cc.png)

## **<font style="color:rgb(0, 0, 0);">mPLUG-Owl3</font>**
项目地址：https://github.com/X-PLUG/mPLUG-Owl/

mPLUG系列在多模态大模型领域产出了多项研究工作。从mPLUG-Owl初代模型引入了视觉对齐-语言模型微调的训练模式，到mPLUG-Owl2通过模块化的模态自适应解决模态拉扯，再到mPLUG-DocOwl通过切图建模高分辨率。这一系列模型一直在探索更为高效有效的多模态大语言模型。

尽管近年包括mPLUG-Owl在内的主流多模态大模型在多种单图任务上取得了一系列进展，当前对于多模态大模型来说，多图长序列输入仍然是一个极具挑战性的场景。针对上述问题，阿里通义实验室提出通用多模态大模型mPLUG-Owl3，该模型能够在支持多图长序列输入的同时，兼顾性能和效率。为实现这一点，作者提出轻量级的hyper attention模块，实现视觉和语言信息的高效自适应融合，在单图、多图、视频等多达14个benchmark上表现出SOTA性能<font style="color:rgba(0, 0, 0, 0.85);">。</font>

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472159579-2a692c40-fadd-41a7-8a2c-82d381b99b04.webp)

## **OVIS**
项目地址：[https://github.com/AIDC-AI/Ovis](https://github.com/AIDC-AI/Ovis?spm=ata.21736010.0.0.7bcb43179Aefhs)

Ovis是阿里国际AI团队发布的一款多模态大模型，借鉴了LLM中的文本嵌入策略，引入了可学习的视觉嵌入表，将连续的视觉特征先转换为概率化的视觉token，再经由视觉嵌入表多次索引加权得到结构化的视觉嵌入。评测结果显示：Ovis在十余项多模态基准测试中均优于主流同尺寸开源MLLM。

**<font style="color:rgb(51, 51, 51);">主要特点:</font>**

1、创新架构设计：可学习的视觉嵌入词表：首次引入，将连续的视觉特征转换为概率化的视觉token，再经由视觉嵌入词表加权生成结构化的视觉嵌入，克服了大部分MLLM中MLP连接器架构的局限性，大幅提升多模态任务表现。

2、高分图像处理：动态子图方案：支持处理极端长宽比的图像，兼容高分辨率图像，展现出色的图像理解能力。

3、全面数据优化：多方向数据集覆盖：全面覆盖Caption、VQA、OCR、Table、Chart等各个多模态数据方向，显著提升多模态问答、指令跟随等任务表现。

4、卓越模型性能：Ovis展现出了优异的榜单表现。在多模态权威综合评测Opencompass上，Ovis1.6-Gemma2-9B在30B参数以下的模型中取得了综合排名第一，超过了Qwen2-VL-7B、MiniCPM-V-2.6等模型。尤其在数学问答等方向表现媲美70B参数模型；在幻觉等任务中，Ovis-1.6的幻觉现象和错误率显著低于同级别的模型，展现了更高的生成文本质量和准确性。

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1733472160172-1beb9c1a-71a7-4915-bf68-ffc2396c2cf9.png)

## Florence
### <font style="color:rgb(0, 0, 0);">Florence2</font>
:::success
**<font style="color:rgb(51, 51, 51) !important;">背景：</font>**<font style="color:rgb(51, 51, 51) !important;">我们已经看到了用于分类的CLIP模型、用于对象检测的Grounding DINO和用于分割的SAM等模型，每种模型在其各自领域都表现出色。</font>**<font style="color:#74B602;">但是，我们是否能够开发一个能够同时处理所有这些任务的单一模型呢？</font>**

:::

:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51) !important;">Florence-2模型：</font>**<font style="color:#ED740C;">一种新颖的开源视觉语言模型（VLM），旨在处理各种视觉和多模型任务，包括字幕识别、对象检测、分割和OCR等内容。</font>**

:::

:::color5
**<font style="color:#601BDE;">1.训练数据</font>**

:::

<font style="color:rgb(51, 51, 51);">为了训练Florence-2模型，研究人员需要一个全面、大规模、高质量的多任务数据集，覆盖了各种图像数据。鉴于这种数据的稀缺性，他们由此创建了全新的多任务图像数据集——FLD-5B。</font>

<font style="color:rgb(51, 51, 51);">这一数据集中包含了1.26亿张图像、5亿个文本标注、13亿个文本-图像区域标注，以及36亿个文本短语-图像区域标注，跨横跨了不同的任务。</font>

**<font style="color:rgb(51, 51, 51);">数据格式</font>**

<font style="color:rgb(51, 51, 51) !important;">受大型语言模型的启发，Florence-2被设计为一种序列到序列的模型。它将图像和文本指令作为输入，并输出文本结果。输入或输出文本可以表示纯文本或图像中的区域。区域格式因任务而异：</font>

+ <font style="color:rgb(51, 51, 51) !important;">边界框：“<X1><Y1><X2><Y2>”用于对象检测任务。这些标记表示长方体左上角和右下角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">四边框：“<X1><Y1><X2><Y2><X3><Y3><X4><Y4>”用于文本检测，使用包围文本的四个角的坐标。</font>
+ <font style="color:rgb(51, 51, 51) !important;">多边形：“<X1><Y1><Xn><Yn>'用于分割任务，其中坐标按顺时针顺序表示多边形的顶点。</font>

:::color5
**<font style="color:#601BDE;">2.数据引擎流程</font>**

:::

<font style="color:rgb(51, 51, 51);">Florence-2数据引擎一共包含三个重要环节：</font>

<font style="color:rgb(51, 51, 51);">1) 使用专业模型进行初始标注</font>

<font style="color:rgb(51, 51, 51);">2) 数据过滤，纠正错误并移除无关标注</font>

<font style="color:rgb(51, 51, 51);">3) 迭代式的数据优化过程</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340588984-846de6c7-1166-4d52-8b0a-204334b652c6.png)

<font style="color:rgb(51, 51, 51);">FLD-5B中的每一张图像都由Florence数据引擎标注了文本、图像区域-文本对以及文本短语-图像区域三元组，涵盖了多个空间层次、从概括到详细的渐进粒度，以及多语义，让模型从不同角度实现了更全面的视觉理解能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340643905-62b28ba5-47b7-4fac-a796-6fa3685c0554.png)

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51) !important;">Florence-2模型是使用标准“编码器-解码器”转换器架构构建的。</font>

+ <font style="color:rgb(51, 51, 51) !important;">输入图像由DaViT视觉编码器嵌入。</font>
+ <font style="color:rgb(51, 51, 51) !important;">文本提示使用BERT嵌入，利用扩展的标记器和单词嵌入层。</font>
+ <font style="color:rgb(51, 51, 51) !important;">视觉和文本嵌入都是连接在一起的。</font>
+ <font style="color:rgb(51, 51, 51) !important;">这些级联的嵌入由基于转换器的多模型编码器-解码器处理，以生成响应。</font>
+ <font style="color:rgb(51, 51, 51) !important;">在训练过程中，该模型最小化交叉熵损失，类似于标准语言模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340494596-586f7a45-498c-4a88-be4d-2c3010734e80.png)



### <font style="color:rgb(0, 0, 0);">Florence-VL</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">微软研究院提出Florence-VL多模态模型，利用生成式视觉编码器Florence-2和深度广度融合机制（</font>[<font style="color:rgb(9, 64, 142);">DBFusion</font>](https://zhida.zhihu.com/search?content_id=251493745&content_type=Article&match_order=1&q=DBFusion&zhida_source=entity)<font style="color:rgb(25, 27, 31);">），高效整合细粒度和高层视觉特征，并在25个基准测试中取得领先性能。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340819169-1e9c30fd-7430-493f-924c-61d853669100.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ <font style="color:rgb(25, 27, 31);">统一视觉编码：单个 vision encoder 降低了复杂性，同时保持了特定任务的适应性。</font>
+ <font style="color:rgb(25, 27, 31);">特定任务的灵活性：基于 prompt 的机制支持各种应用，包括 OCR 和 grounding。</font>
+ <font style="color:rgb(25, 27, 31);">增强的融合策略：DBFusion 确保了 depth 和 breadth features 的丰富组合，捕捉粒度和上下文细节。</font>
+ <font style="color:rgb(25, 27, 31);">卓越的基准测试结果：Florence-VL 在 25 个 benchmarks 中处于领先地位，实现了 2.98 的 alignment loss。</font>
+ <font style="color:rgb(25, 27, 31);">训练效率：在预训练期间 fine-tune 整个架构可增强多模态对齐，从而产生更好的任务结果。</font>

:::color5
**<font style="color:#601BDE;">2.技术原理</font>**

:::

+ [**<font style="color:rgb(9, 64, 142);">生成式视觉编码器</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%94%9F%E6%88%90%E5%BC%8F%E8%A7%86%E8%A7%89%E7%BC%96%E7%A0%81%E5%99%A8&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：使用Florence-2作为视觉编码器，基于不同的任务提示生成视觉特征，适用于多种视觉任务。</font>
+ [**<font style="color:rgb(9, 64, 142);">特征融合架构</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%89%B9%E5%BE%81%E8%9E%8D%E5%90%88%E6%9E%B6%E6%9E%84&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：引入新颖的特征融合架构，将从Florence-2提取的视觉特征与预训练的语言模型相结合。</font>
+ **<font style="color:rgb(25, 27, 31);">深度-广度融合（DBFusion）</font>**<font style="color:rgb(25, 27, 31);">：</font>
+ **<font style="color:rgb(25, 27, 31);">深度</font>**<font style="color:rgb(25, 27, 31);">：整合来自不同层次的视觉特征，捕捉从低级到高级的概念细节。</font>
+ **<font style="color:rgb(25, 27, 31);">广度</font>**<font style="color:rgb(25, 27, 31);">：使用多个任务特定的视觉特征，每个特征强调输入图像中的不同感知信息。</font>
+ [**<font style="color:rgb(9, 64, 142);">端到端预训练</font>**](https://zhida.zhihu.com/search?content_id=251398051&content_type=Article&match_order=1&q=%E7%AB%AF%E5%88%B0%E7%AB%AF%E9%A2%84%E8%AE%AD%E7%BB%83&zhida_source=entity)<font style="color:rgb(25, 27, 31);">：整个模型进行端到端预训练，实现视觉和语言模态之间的最佳对齐。</font>
+ **<font style="color:rgb(25, 27, 31);">微调</font>**<font style="color:rgb(25, 27, 31);">：在预训练后，对投影层和语言模型进行微调，适应特定的下游任务。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(34, 34, 34);">在多种视觉编码器对比实验里，Florence-2 就像一匹黑马脱颖而出。实验测不同视觉编码器与语言模型的跨模态对齐能力，结果 Florence-2 显示出更优的能力，就像在一场赛跑里，它跑得比其他选手都快。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741340931207-1cc91661-5348-44da-9191-ad6c94662795.png)



## LLAVA系列
### LLAVA
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">多模态需求</font>**<font style="color:rgb(51, 51, 51);">：随着AI在视觉-语言任务（如图像问答、图文生成）中的需求增长，传统单模态模型难以满足复杂场景。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">现有不足</font>**<font style="color:rgb(51, 51, 51);">：早期多模态模型（如Flamingo）依赖海量数据与算力，且跨模态对齐效率低。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">LLaVA定位</font>**<font style="color:rgb(51, 51, 51);">：基于开源LLM（如Vicuna）与视觉编码器（CLIP-ViT），通过轻量级设计实现高效视觉-语言对齐。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741078830518-06b4da4b-1f59-4f2e-8ba9-5332ebaf8480.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">简单投影层</font>**<font style="color:rgb(51, 51, 51);">：用线性层或MLP将图像特征映射到文本嵌入空间，无需复杂跨模态架构。</font>
+ **<font style="color:rgb(51, 51, 51);">两阶段训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">阶段1</font>**<font style="color:rgb(51, 51, 51);">：冻结视觉与语言模型，仅训练投影层，实现模态对齐。</font>
    - **<font style="color:rgb(51, 51, 51);">阶段2</font>**<font style="color:rgb(51, 51, 51);">：端到端微调，增强多模态交互能力。</font>
+ **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：利用GPT-4生成高质量指令数据，降低标注成本。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉数据</font>**<font style="color:rgb(51, 51, 51);">：COCO、Visual Genome等公开图像数据集。</font>
+ **<font style="color:rgb(51, 51, 51);">文本数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">对齐数据</font>**<font style="color:rgb(51, 51, 51);">：图像-描述对（如COCO Captions）。</font>
    - **<font style="color:rgb(51, 51, 51);">指令数据</font>**<font style="color:rgb(51, 51, 51);">：GPT-4生成的问答对（如“描述图中场景并推测事件原因”）。</font>
+ **<font style="color:rgb(51, 51, 51);">格式</font>**<font style="color:rgb(51, 51, 51);">：多轮对话（User: [图像] + 问题；Assistant: 回答）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：CLIP-ViT-L/14，提取图像特征（每图→</font>`<font style="color:rgb(51, 51, 51);">[N, d_vis]</font>`<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：线性层或MLP，将</font>`<font style="color:rgb(51, 51, 51);">d_vis</font>`<font style="color:rgb(51, 51, 51);">维特征映射到语言模型嵌入空间</font>`<font style="color:rgb(51, 51, 51);">d_txt</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">语言模型</font>**<font style="color:rgb(51, 51, 51);">：Vicuna（LLaMA微调版），处理文本与投影后的视觉特征。</font>
+ **<font style="color:rgb(51, 51, 51);">输入拼接</font>**<font style="color:rgb(51, 51, 51);">：图像特征与文本嵌入拼接为序列输入语言模型。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **阶段1 - 特征对齐**：
    - <font style="color:rgb(51, 51, 51);">冻结ViT和LLM，</font>**<font style="color:#ED740C;">仅训练投影层</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">目标：最小化图文匹配损失（如对比学习）。</font>
    - <font style="color:rgb(51, 51, 51);">数据：图像-文本对，将CC3M过滤为595K图像文本对。</font>
2. **阶段2 - 端到端微调**：
    - <font style="color:rgb(51, 51, 51);">冻结视觉，</font>**<font style="color:#ED740C;">联合优化投影层与LLM</font>**<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">目标：生成任务的交叉熵损失。</font>
    - <font style="color:rgb(51, 51, 51);">数据：指令数据（GPT-4生成的多轮对话），158K图文指令数据，来自COCO图片。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">计算高效（复用预训练模型，轻量投影层）。</font>
+ <font style="color:rgb(51, 51, 51);">支持复杂视觉推理（如因果推断、细节描述）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">图像分辨率固定，细节处理有限。</font>
+ <font style="color:rgb(51, 51, 51);">依赖语言模型生成能力，可能产生幻觉回答。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">：用户上传图片提问，模型生成解释。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：解析教科书图表并生成讲解。</font>
+ **<font style="color:rgb(51, 51, 51);">无障碍技术</font>**<font style="color:rgb(51, 51, 51);">：为视障用户描述场景。</font>
+ **<font style="color:rgb(51, 51, 51);">内容审核</font>**<font style="color:rgb(51, 51, 51);">：结合图像与文本进行违规内容检测。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">增强视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：使用更高分辨率ViT或SAM分割模型。</font>
+ **<font style="color:rgb(51, 51, 51);">动态投影层</font>**<font style="color:rgb(51, 51, 51);">：引入注意力机制替代简单线性层。</font>
+ **<font style="color:rgb(51, 51, 51);">混合数据训练</font>**<font style="color:rgb(51, 51, 51);">：加入视频数据提升时序理解能力。</font>
+ **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：基于人类反馈（RLHF）优化生成结果。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import AutoTokenizer, CLIPModel, LlamaForCausalLM

class LLaVA(torch.nn.Module):
    def __init__(self, llm_name="vicuna-7b", clip_name="openai/clip-vit-large-patch14"):
        super().__init__()
        self.vision_encoder = CLIPModel.from_pretrained(clip_name).visual
        self.tokenizer = AutoTokenizer.from_pretrained(llm_name)
        self.llm = LlamaForCausalLM.from_pretrained(llm_name)
        self.proj = torch.nn.Linear(1024, self.llm.config.hidden_size)  # 投影层

    def forward(self, images, input_ids, attention_mask):
        # 提取图像特征
        vis_features = self.vision_encoder(images).last_hidden_state.mean(dim=1)
        # 投影到文本空间
        vis_embeds = self.proj(vis_features).unsqueeze(1)
        # 拼接文本嵌入
        text_embeds = self.llm.get_input_embeddings()(input_ids)
        inputs_embeds = torch.cat([vis_embeds, text_embeds], dim=1)
        # 生成输出
        outputs = self.llm(inputs_embeds=inputs_embeds, attention_mask=attention_mask)
        return outputs.logits

# 示例调用
model = LLaVA()
images = torch.randn(1, 3, 224, 224)  # 输入图像
input_ids = model.tokenizer("Describe this image:", return_tensors="pt").input_ids
logits = model(images, input_ids, attention_mask=None)

```

```python
# 两阶段训练示例
optimizer = torch.optim.AdamW([
    {'params': model.proj.parameters(), 'lr': 1e-3},  # 阶段1仅训练投影层
    {'params': model.llm.parameters(), 'lr': 2e-5}     # 阶段2解冻LLM
])

for epoch in range(epochs):
    for images, texts in dataloader:
        inputs = tokenizer(texts, padding=True, return_tensors="pt")
        logits = model(images, inputs.input_ids, inputs.attention_mask)
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, logits.shape[-1]), inputs.input_ids.view(-1)
        )
        loss.backward()
        optimizer.step()

```

#### LLAVA与CLIP对齐的对比
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">CLIP</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐 是其核心能力，通过</font>**<font style="color:#ED740C;">对比学习（Contrastive Learning）</font>**<font style="color:rgb(25, 27, 31);">将图像和文本映射到统一的语义空间。</font>

**<font style="color:rgb(25, 27, 31);">LLaVA</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐的核心是通过一个</font>**<font style="color:#ED740C;">轻量级线性投影层将视觉特征映射到语言模型的词嵌入空间</font>**<font style="color:rgb(25, 27, 31);">，结合两阶段训练策略实现高效对齐。以下是详细的技术分解：</font>

**<font style="color:rgb(51, 51, 51);">参考</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://zhuanlan.zhihu.com/p/27728623876](https://zhuanlan.zhihu.com/p/27728623876)

:::

:::color5
**<font style="color:#601BDE;">1.CLIP多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849995591-667a0c79-beab-443f-931c-f351159cd7c4.png)

1. 模型结构
    - <font style="color:rgb(25, 27, 31);">图像编码器：例如 Vision Transformer（ViT）或 ResNet，将图像编码为特征向量。</font>
    - <font style="color:rgb(25, 27, 31);">文本编码器：例如 Transformer，将文本编码为特征向量。</font>
2. 对齐方法
    - <font style="color:rgb(25, 27, 31);">输入：</font>
        * <font style="color:rgb(25, 27, 31);">图像：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[img_1, img_2, ..., img_N]</font>`
        * <font style="color:rgb(25, 27, 31);">文本：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[text_1, text_2, ..., text_N]</font>`
    - <font style="color:rgb(25, 27, 31);">步骤：</font>
        * **<font style="color:rgb(25, 27, 31);">a.特征提取：</font>**
            + <font style="color:rgb(25, 27, 31);">图像特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">I = image_encoder(img_1), ..., image_encoder(img_N)</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">→ 维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
            + <font style="color:rgb(25, 27, 31);">文本特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">T = text_encoder(text_1), ..., text_encoder(text_N)</font>`<font style="color:rgb(25, 27, 31);"> → 维度 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
        * **<font style="color:rgb(25, 27, 31);">b.相似度计算：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">计算所有图像和文本的余弦相似度矩阵</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S</font>`<font style="color:rgb(25, 27, 31);">，维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, N]</font>`<font style="color:rgb(25, 27, 31);">：</font>

```plain
S[i][j] = cosine_similarity(I[i], T[j])
```

    - <font style="color:rgb(25, 27, 31);">理想情况下，对角线元素 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S[i][i]</font>`<font style="color:rgb(25, 27, 31);"> 应最大（匹配对），非对角线元素应较小（不匹配对）</font>
        * **<font style="color:rgb(25, 27, 31);">c.对比损失（InfoNCE）：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">对每个图像</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">i</font>`<font style="color:rgb(25, 27, 31);">，计算其与所有文本的相似度，通过 softmax 得到概率分布：</font>

```plain
p_image2text(i) = exp(S[i][i]/τ) / sum_{j=1}^N exp(S[i][j]/τ)
```

        * <font style="color:rgb(25, 27, 31);">对每个文本</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">j</font>`<font style="color:rgb(25, 27, 31);">，同理计算</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">p_text2image(j)</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">总损失为两个方向的交叉熵之和：</font>
        * <font style="color:rgb(25, 27, 31);">其中 τ 是温度参数，控制分布集中程度。</font>

```plain
loss = -1/(2N) * sum_{i=1}^N [log(p_image2text(i)) + log(p_text2image(i))]
```

:::color5
**<font style="color:#601BDE;">2.LLAVA多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849977575-d145922b-3207-4c22-a51a-e5519ce67e37.png)

1. **模型架构**
    1. <font style="color:rgb(25, 27, 31);">视觉编码器：CLIP-ViT-L/14（输出维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[H, W, D_img] = [16, 16, 1024]</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    2. <font style="color:rgb(25, 27, 31);">线性投影层（对齐模块）：单层全连接网络（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj ∈ R^{D_img × D_text}</font>`<font style="color:rgb(25, 27, 31);">），将图像特征转换为语言模型兼容的维度（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text=4096</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    3. <font style="color:rgb(25, 27, 31);">语言模型：</font>[<font style="color:rgb(9, 64, 142);">Vicuna</font>](https://zhida.zhihu.com/search?content_id=254568449&content_type=Article&match_order=1&q=Vicuna&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（LLaMA架构的指令微调版本），词嵌入维度为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text</font>`<font style="color:rgb(25, 27, 31);">。</font>
2. **对齐步骤**
    1. **<font style="color:rgb(25, 27, 31);">视觉特征处理</font>**
        * <font style="color:rgb(25, 27, 31);">输入图像：尺寸</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">224×224</font>`<font style="color:rgb(25, 27, 31);">，通过ViT划分为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">16×16</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个patch，输出特征图</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[16×16, 1024]</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">特征扁平化：将空间维度合并为序列，得到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×1024</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的特征矩阵。</font>
        * <font style="color:rgb(25, 27, 31);">线性投影：通过 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj</font>`<font style="color:rgb(25, 27, 31);"> 将每个patch特征转换为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">4096</font>`<font style="color:rgb(25, 27, 31);"> 维，得到 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);"> 的视觉token序列。</font>
    2. **<font style="color:rgb(25, 27, 31);">步骤2：与文本token拼接</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">将视觉token（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);">）与文本token（如问题“描述这张图片”）拼接，形成联合输入序列。</font>
        * <font style="color:rgb(25, 27, 31);">示例：输入序列 = [IMG_1, IMG_2, ..., IMG_256] + [Q1, Q2, ..., Qn]</font>
        * <font style="color:rgb(25, 27, 31);">语言模型（Vicuna）将此序列视为“多模态prompt”，自回归生成答案。</font>
    3. **<font style="color:rgb(25, 27, 31);">预训练（特征对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：对齐视觉与语言特征，使投影后的视觉token能被语言模型“理解”。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用约 600K 图像-文本对（来自CC3M等），构造单轮指令数据（如“请描述图像” + 人工标注描述）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">冻结参数：</font>**<font style="color:#ED740C;">视觉编码器和语言模型权重固定</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">仅训练投影层：通过最小化语言模型的交叉熵损失，优化视觉到文本的映射。</font>
            + <font style="color:rgb(25, 27, 31);">关键公式：</font>
    4. **<font style="color:rgb(25, 27, 31);">阶段2：指令微调（任务对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：提升模型对复杂指令（如推理、问答）的响应能力。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用158K GPT-4生成的指令-答案对（涵盖描述、推理、对话等任务）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">解冻语言模型：</font>**<font style="color:#ED740C;">微调语言模型参数（LoRA或全参数微调）</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">联合优化：投影层和语言模型共同更新，强化跨模态交互。</font>
            + <font style="color:rgb(25, 27, 31);">示例任务：</font>
                - <font style="color:rgb(25, 27, 31);">输入：图像 + “图中的小狗是什么颜色？”</font>
                - <font style="color:rgb(25, 27, 31);">输出：语言模型需结合视觉token（如“黑色毛发”）生成答案“黑色”。</font>

### LLAVA-Next
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>LLaVA作为最早一批出现的多模态大模型，其模型结构与训练策略对于现在的多模态模型发展产生了巨大的影响。

**github**：[https://github.com/haotian-liu/LLaVA/tree/main](https://github.com/haotian-liu/LLaVA/tree/main)

:::

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472160548-c481673d-772d-4250-afff-81913d073d68.webp)

:::color5
**<font style="color:#601BDE;">1.版本对比</font>**

:::

| <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">模型版本</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava1.5</font> | <font style="color:rgba(0, 0, 0, 0.9);background-color:rgb(242, 243, 245);">LLava-Next(1.6)</font> |
| :--- | :--- | :--- | :--- |
| <font style="color:rgba(0, 0, 0, 0.9);">输入分辨率</font> | <font style="color:rgba(0, 0, 0, 0.9);">224*224</font> | <font style="color:rgba(0, 0, 0, 0.9);">336*336</font> | <font style="color:rgba(0, 0, 0, 0.9);">336*{2x2， 1x{2,3,4}, {2,3,4} x 1}的网格配置</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">视觉编码器</font> | <font style="color:rgba(0, 0, 0, 0.9);">CLIP-L/14</font> | **<font style="color:rgba(0, 0, 0, 0.9);">CLIP-ViT-L-336px</font>** | **<font style="color:rgba(0, 0, 0, 0.9);">CLIP-ViT-L-336px</font>** |
| <font style="color:rgba(0, 0, 0, 0.9);">连接器</font> | <font style="color:rgba(0, 0, 0, 0.9);">一个全连接层</font> | <font style="color:rgba(0, 0, 0, 0.9);">2层MLP</font> | <font style="color:rgba(0, 0, 0, 0.9);">2层MLP</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">LLM</font> | <font style="color:rgba(0, 0, 0, 0.9);">llama1-13B、7B</font> | <font style="color:rgba(0, 0, 0, 0.9);">Vicuna-1.5（7B和13B）</font> | <font style="color:rgba(0, 0, 0, 0.9);">Vicuna-1.5（7B和13B）</font><br/><font style="color:rgba(0, 0, 0, 0.9);">Mistral 7B</font><br/><font style="color:rgba(0, 0, 0, 0.9);">Nous-Hermes-2-Yi-34B</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">预训练数据集</font> | **<font style="color:rgba(0, 0, 0, 0.9);">CC3M（595K）</font>** | | |
| <font style="color:rgba(0, 0, 0, 0.9);">指令微调数据集</font> | <font style="color:rgba(0, 0, 0, 0.9);">158K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（使用COCO生成的对话、描述、复杂推理数据集）</font> | <font style="color:rgba(0, 0, 0, 0.9);">665K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（在前一版基础上增加ShareGPT数据集、学术导向的VQA数据集、OCR数据集、Region-level的VQA数据集）</font> | <font style="color:rgba(0, 0, 0, 0.9);">760K</font><br/><font style="color:rgba(0, 0, 0, 0.9);">（在前一个版本基础上</font>**<font style="color:rgba(0, 0, 0, 0.9);">移除</font>**<font style="color:rgba(0, 0, 0, 0.9);">TextCaps数据集、新增LAION-GPT-V、ShareGPT-4V、先上分收集的LLaVA demo数据集、DocVQA和SynDog-EN的OCR数据集、以及ChartQA、DVQA和AI2D等表格QA数据集）</font> |


:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

**<font style="color:rgb(51, 51, 51);">缺点</font>**

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

<font style="color:rgb(51, 51, 51);"></font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::



:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python

```

在LLAVA1.5的基础上，LLAVA-NEXT进一步支持了高分辨率图像。它支持三种宽高比，分别为 672x672，336x1344，1344x336。（Vision Encoder 的输入是 336px）使用 Hermes-Yi-34B 为 LLM 的 LLaVA-NeXT 更是在多项评测标准上超过了 Gemini-Pro。

此外，LLaVA-NeXT 真正应用了 AnyRes 技术。如下图所示，图片一方面按照 2x2 进行分割并分别编码，最后合并展平，输入给 LLM。另一方面，图片会进行降采样并直接进行编码，从而为 LLM 提供图片的全局信息。分割方式具体包含 2x2，1x2，1x3，1x4，2x1，3x1 和 4x1。

在使用了更大的 LLM 后，LLaVA-NeXT 的能力迎来了进一步强化。此处的 LLaVA-NeXT 使用了 Qwen1.5-110B、Qwen1.5-72B、LLaMA3-8B 作为 LLM，其中使用了 Qwen1.5-110B 的 LLaVA-NeXT 的模型表现更是直追 GPT4-V。

![](https://cdn.nlark.com/yuque/0/2024/webp/29769680/1733472160548-c481673d-772d-4250-afff-81913d073d68.webp)



### Dynamic LLAVA <font style="color:#D22D8D;">（by草莓师姐）</font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>本文主要围绕以 LLaVA 为范式的多模态大模型展开研究。一个多模态大模型的推理过程可以分为预填充和解码两个阶段：

+ **预填充阶段**：不同模态的特征被映射到与大语言模型（LLM）输入 embedding 相同的特征分布空间中。这些多模态特征与文本 token 会一起被大语言模型处理，以生成初始输出文本 token。以图片理解场景为例，该阶段主要处理输入的图片和文本格式的问题。
+ **解码阶段**：预填充阶段生成的所有 token 以及后续生成的所有输出文本 token，将被用于自回归生成，从而产生完整的输出。同样以图片理解场景为例，该阶段生成针对整个问题的完整回答。

:::

:::color3
**简介：**<font style="color:#000000;">针对上述问题，论文认为：为了实现真正的全阶段推理加速，</font>**<font style="color:#ED740C;">不仅需要对预填充阶段的视觉 token 进行剪枝，还必须对解码阶段输出的文本 token 进行稀疏化处理</font>**<font style="color:#000000;">，限制参与自回归运算的 token 数量。 </font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:#000000;"> </font>**<font style="color:#000000;">Dynamic-LLaVA</font>**<font style="color:#000000;">是针对多模态大模型提出的的视觉-语言上下文稀疏化推理加速框架。该框架能够集成到多模态大模型推理的不同阶段中，实现以下目标：</font>

+ **<font style="color:#000000;">显著降低预填充阶段计算开销：</font>**<font style="color:#000000;">通过优化视觉 token 的处理方式，减少不必要的计算。</font>
+ **<font style="color:#000000;">提升解码阶段的推理效率：</font>**<font style="color:#000000;">无论是否使用 KV Cache，都能减少计算开销，提高推理速度。</font>
+ **<font style="color:#000000;">保持性能优势：</font>**<font style="color:#000000;">在视觉理解任务上几乎不损失性能；在长文本输出场景中，生成能力也几乎不受影响。</font>

<font style="color:#000000;">通过这些创新，Dynamic-LLaVA 为多模态大模型的高效推理提供了一种全新的解决方案。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Osilly/dynamic_llava](https://github.com/Osilly/dynamic_llava)

**paper：**[**Dynamic-LLaVA: Efficient Multimodal Large Language Models via Dynamic Vision-language Context Sparsification**](https://arxiv.org/pdf/2412.00876)

**参考：**[**https://mp.weixin.qq.com/s/2SbbAlLxZG9Ub_lZf8YVDw**](https://mp.weixin.qq.com/s/2SbbAlLxZG9Ub_lZf8YVDw)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760547508-71b3e2af-2994-4252-b6b0-b1f4104ba48f.png)

<font style="color:rgb(136, 136, 136);">▲ 图6：Dynamic-LLaVA-13B 在 LVIS-VQA（single-round）上的推理结果展示。图片的白色部分表示该位置的图像块被丢弃，文字中的灰色部分表示其在稀疏化过程中被丢弃，这表示它们不参与后续的自回归解码过程，但在模型的输出中都被完整保留</font>

图 6 中展示了 Dynamic-LLaVA-13B 在 LVIS-VQA（single-round）上的推理结果，以及对视觉和文本 token 的稀疏化情况。

可视化结果表明，视觉 token 部分的主要信息得以保留；**<font style="color:#74B602;">文本 token 中，一些不影响整体语义理解的连词、介词等被丢弃。这表明 Dynamic-LLaVA 能够实现关键的视觉、语义信息的保留，从而保证了模型整体的性能。</font>**

:::color5
**<font style="color:#601BDE;">1.多模态大模型的推理瓶颈 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745759717189-9fed35a4-9ac4-4337-8103-c2fad1a515bf.png)

<font style="color:rgb(63, 63, 63);">现有的多模态大模型大多以基于解码器架构的大语言模型（LLM）为核心，这些模型通常拥有庞大的参数规模。在生成输出文本 token 的过程中，模型计算负担会逐渐加重，导致对计算资源的巨大消耗。</font>

<font style="color:rgb(63, 63, 63);">为了提升推理速度，现有模型通常会在解码过程中运用 KV Cache 技术，通过存储并复用之前计算的 KV 激活值来减少重复计算。然而，如图 1（B）所示，</font>**<font style="color:#117CEE;">即使使用了 KV Cache，LLaVA 在输出 token 不断增加时，仍会迅速面临 GPU 显存耗尽的问题</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">与文本不同，视觉信息往往包含大量冗余。因此，许多方法尝试通过减少视觉上下文来加速多模态大模型的推理，即对预填充阶段的视觉 token 进行剪枝处理。但这种方法存在局限性：</font>**<font style="color:#117CEE;">其主要提升了多模态大语言模型在预填充阶段的推理效率，而在解码阶段，其效率提升会逐渐减弱</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">如图 1（B）和（C）所示，FastV 这种针对视觉 token 剪枝的方法，虽然相较于原始的 LLaVA 能够节省一定的 GPU 显存和计算开销（FLOPs），但当输出 token 数接近 5K 时，它仍然会遭遇计算资源瓶颈。</font>

<font style="color:rgb(63, 63, 63);">此外，FastV 和原始 LLaVA 的曲线斜率基本一致，这表明在长输出的解码阶段，这类方法并没有显著的推理效率优势。因此，</font>**<font style="color:#117CEE;">仅通过减少预填充阶段的视觉 token，在输出文本 token 数量远超视觉 token 时，难以实现整个推理效率的显著提升。</font>**

:::color5
**<font style="color:#601BDE;">2.方法 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745759731667-7e11e19d-ef31-4ee6-9fe7-ba8277c4b62c.png)

如图 2 所示，Dynamic-LLaVA 可以集成到多模态大模型推理流程中的不同阶段。具体而言，在预填充阶段，该框架**<font style="color:#74B602;">对视觉 token 执行精准剪枝操作，剔除冗余信息</font>**；在不使用 KV Cache 的解码阶段，**<font style="color:#74B602;">限制参与自回归运算的视觉与输出文本 token 数量</font>**，避免不必要的计算负担。

而在使用 KV Cache 的解码阶段，Dynamic-LLaVA 则动态调控 KV Cache，自适应判断是否将当前输出文本 token 的 KV 激活值纳入 KV Cache，优化资源利用效率。

为了使模型适应这种全新的稀疏化推理模式，Dynamic-LLaVA 在预训练的 LLaVA-1.5 基础上进行了 1 个 epoch 的监督微调（SFT），确保模型能够高效地运行在稀疏化的推理路径上。

:::color5
**<font style="color:#601BDE;">3.Prefill 预填充 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">在预填充阶段，我们对输入的视觉 token 进行稀疏化操作。如图 2 左侧部分所示，我们引入一个</font>**<font style="color:#74B602;">可训练的轻量化的图像预测器（Image Predictor），来判断应当丢弃哪些视觉 token</font>**<font style="color:rgb(63, 63, 63);">。该图像预测器的结构如下图：</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759451131-edf617a4-e369-4354-8a26-45e25ae7e9a5.webp)

<font style="color:rgb(136, 136, 136);">▲ 图3：图像预测器的结构示意图 </font>

<font style="color:rgb(63, 63, 63);">图像预测器会对每个视觉 token 产生</font>**<font style="color:#74B602;">“决策分数”，以决定对哪些视觉 token 进行保留</font>**<font style="color:rgb(63, 63, 63);">。</font>

<font style="color:rgb(63, 63, 63);">在端到端训练中，视觉 token 的剪枝通过 0-1 二值化的掩码操作实现（具体过程见 2.4 节）。</font>

<font style="color:rgb(63, 63, 63);">在实际推理阶段中，通过保留“决策分数”前 k 大的视觉 token（即图 2 左侧部分的 “Yes” 分支），实现视觉 token 数量减少，以实现推理加速。</font>

:::color5
**<font style="color:#601BDE;">4.解码阶段 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(0, 0, 0);">不使用 KV Cache 的解码过程：</font>**

<font style="color:rgb(63, 63, 63);">对于视觉 token，采用和上一小节相同的做法，进行稀疏化处理。</font>

<font style="color:rgb(63, 63, 63);">对于输出的文本 token，分两类进行处理：</font>

+ <font style="color:rgb(63, 63, 63);">最后一个输出的文本 token（即图 2 中间部分的 “Last output text token”），不进行任何处理，完整输入 LLM 的 decoder 层进行计算。这样做的目的是保证模型的输出内容是连贯的，产生新的输出文本 token 时，始终保证自回归运算包含上一个输出文本 token。</font>
+ <font style="color:rgb(63, 63, 63);">对其他历史的输出文本 token 进行稀疏化操作，其形式类似于对视觉 token 的处理。引入一个结构如下图的输出预测器（Output Predictor），给出每个输出文本 token 的“决策分数”，以决定当前产生新的输出内容时，应当包括哪些文本 token 进行自回归运算。图 2 中间部分的 “Yes” 分支，表明保留的输出文本 token。</font>

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759769837-3c8c7f1e-56ad-48ba-8ac2-9b9149e01e02.webp)

<font style="color:rgb(136, 136, 136);">▲ 图4：输出预测器的结构示意图 </font>

**<font style="color:rgb(63, 63, 63);">使用 KV Cache 的解码过程：</font>**

<font style="color:rgb(63, 63, 63);">KV Cache 是节省冗余计算的一个关键推理加速技术，其思想是“用 GPU 显存的空间换计算时间”。显而易见的是，KV Cache 也并非无限大，在长输出情况下，必须丢弃一些 KV Cache 以适应有限的 GPU 显存。</font>

<font style="color:rgb(63, 63, 63);">目前在 LLM 领域已有大量的 KV Cache 压缩方案，以 H</font><sub><font style="color:rgb(63, 63, 63);">2</font></sub><font style="color:rgb(63, 63, 63);">O方法为代表，这一类方法一般基于当前 token 和历史 KV Cache 进行重要性分数计算，以压缩历史 KV Cache。</font>

<font style="color:rgb(63, 63, 63);">与上述方法不同的是，我们对有 KV Cache 的解码阶段的设计，</font>**<font style="color:#74B602;">核心在于“仅判断当前新 token 的 KV 激活是否需要加入 KV Cache 中”。</font>**

<font style="color:rgb(63, 63, 63);">如图 3 右侧所示，对于当前正在处理的新 token（Last output text token），使用和上一部分结构相同的输出预测器，以决定是否加入 KV Cache 集合中。</font>

<font style="color:rgb(63, 63, 63);">这种 “</font>**<font style="color:#74B602;">Online KV Cache 压缩</font>**<font style="color:rgb(63, 63, 63);">”方法，判断是否保留 KV Cache 的过程计算复杂度更低，也更加适应多模态场景。在论文论文附录中，我们详细讨论了我们的方法和现有的 LLM KV Cache 压缩方法的区别。</font>

<font style="color:rgb(63, 63, 63);">需要特别说明的是，和不使用 KV Cache 的解码阶段相同，无论当前处理的 token 是否加入 KV Cache，其都会输入 LLM decoder 层进行计算，以保证输出的连贯性。</font>

:::color5
**<font style="color:#601BDE;">5.端到端训练 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745759991825-80de864e-82c5-4398-a68d-f6a78149d92e.webp)

<font style="color:rgb(136, 136, 136);">▲ 图5：Dynamic-LLaVA 在端到端训练过程中的示意图</font>

<font style="color:rgb(63, 63, 63);">Dynamic-LLaVA 是一个需要训练的多模态大模型推理加速框架。我们基于 LLaVA 进行了一个 epoch 的指令微调，以实现对 token 动态选择的稳定性，保证最终的性能。为了保证端到端训练，在训练阶段的稀疏化操作通过 0-1 二值化掩码实现（在推理中的实现是直接从历史 token 序列中丢弃 token）。</font>

<font style="color:rgb(63, 63, 63);">如图 5 所示，上半部分表示训练中进行 mask 的过程，在得到整个 token 序列的重要性分数后，我们</font>**<font style="color:#74B602;">选取前 k 重要的 token 进行保留，相对应的生成掩码向量，其中 0 对应丢弃的冗余 token（不参与注意力过程的计算），1 对应保留的重要 token</font>**<font style="color:rgb(63, 63, 63);">，进一步基于掩码向量生成注意力过程的掩码矩阵。</font>

<font style="color:rgb(63, 63, 63);">掩码矩阵用来对多头注意力机制进行掩码操作，以确保丢弃的 token 不参与注意力过程的计算。由于二值化操作会导致不可微问题，所以我们借助了 GumbalSoftmax 和梯度直通估计器（Straight Through Estimator, STE）来保证梯度流的正确传播，以进行端到端的训练，如图 5 下半部分所示。</font>

:::color5
**<font style="color:#601BDE;">6.视觉理解能力 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

我们首先评估了 Dynamic-LLaVA 在主要的视觉理解基准的性能，选取了目前主流的多模态大模型推理加速方法进行比较。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760139142-881054ad-07f4-40d0-bf0e-095c62998bd9.png)

<font style="color:rgb(136, 136, 136);">▲ 表1：视觉理解基准效果对比。其中，Free 表示方法是否是 Training-Free 的。Dynamic-LLaVA 的下标 “” 和 “” 分别表示仅对视觉 token 做稀疏化和同时对视觉和文本 token 都做稀疏化（该标识适用于下文所有的表格）</font>

如表 1 所示，Dynamic-LLaVA 在大部分视觉理解任务上取得了优越的性能。和其他对视觉内容稀疏化的方法相比，**<font style="color:#74B602;">Dynamic-LLaVA 在能大幅减小计算复杂度的同时，能够实现相比原始的 LLaVA-1.5 性能几乎不下降。</font>**

此外，在 SciQA、POPE、MME 和 MMBench上，Dynamic-LLaVA 相比 LLaVA-1.5 甚至有一定的性能提升。例如，在 SciQA 任务上，Dynamic-LLaVA 的 7B 和 13B 版本，相较于 LLaVA-1.5 实现了 2.3% 和 0.8% 的性能提升。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760160421-b5bc7293-7bd2-4a77-b8fe-58a7c89bbc40.png)

<font style="color:rgb(136, 136, 136);">▲ 表2：与其他高效视觉 projector 的 SOTA 方法对比</font>

值得一提的是，Dynamic-LLaVA 并没有对 LLaVA-1.5 的视觉 projector 进行修改，就可以**<font style="color:#74B602;">实现大幅降低预填充阶段计算复杂度，同时维持模型性能。</font>**

在表 2 中，和其他针对视觉 projector 做高效设计（以提高推理效率）的 SOTA 方法进行了对比。

相较于其他使用了高效的视觉 projector 的方法，Dynamic-LLaVA 使用和 LLaVA-1.5 相同的 MLP 结构作为视觉 projector，实现了更好的性能，同时也大幅降低了预填充阶段的计算复杂度。

此外，Dynamic-LLaVA 也可以和其他使用高效视觉 projector 的方法集成。例如，表 2 中 Dynamic-LLaVA 使用 TokenPacker 这一高效视觉 projector 的版本，在原始的 TokenPacker 方法基础上，进一步减少了视觉 token。相较于其他基于 TokenPacker 的推理加速方法，性能损失最少。

:::color5
**<font style="color:#601BDE;">7.生成能力 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

现有的视觉理解任务中，一般只要求模型给出简短的回复，这和现实世界中多模态大模型的应用场景仍然存在不小的区别。在现实使用中，多模态大模型多数情况下会被要求生成更长、更细致的描述。

为了和现实世界的场景对齐，评估在 Dynamic-LLaVA 在更长的输出情况下的生成能力和推理效率。我们额外构建了两个评估模型生成能力的基准：

+ LVIS-VQA：基于 LVIS-Instruct4 数据集，选取了 1000 个回答超过 100 个单词的单轮对话样本构成 LVIS-VQA（single round）和 1000 个多轮对话样本（平均回答单词数超过 300）构成 LVIS-VQA（multi-round）；
+ ShareGPT4V-VQA：基于 ShareGPT-4V 数据集，选取了 caption 超过 300 个单词的单论对话样本，平均输出 token 长度超过 1000。

我们以 PPL（Perplexity Metric）指标评估模型生成内容的流畅度、以 METEOR（Metric for Evaluation of Translation with Explicit ORdering）指标评估模型生成内容的质量。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1745760299604-13f39e73-50f1-4fa4-8efc-98a053f0ecf6.png)

<font style="color:rgb(136, 136, 136);">▲ 表3：生成能力基准比较。其中，解码阶段的 TFLOPs 和 Mem.（GPU 显存占用）分别在无/有 KV Cache 的情况下测量得出。PPL 越低越好，METEOR 越高越好</font>

如表 3 所示，相比 LLaVA-1.5，只进行视觉内容稀疏化的 Dynamic-LLaVA 的生成流畅度（PPL）和生成质量（METEOR）几乎没有变化。

同时对视觉和文本进行稀疏化的 Dynamic-LLaVA，PPL 仅变高了 0.3，METEOR 甚至略有提升，而在推理效率上，在无 KV Cache 的解码阶段降低了 ～ 50% 的 TFLOPs，在有 KV Cache 的解码阶段降低了 ～ 50% 的 GPU 显存占用。

实验结果充分表明，**<font style="color:#74B602;">Dynamic-LLaVA 针对视觉和文本同时进行稀疏化，几乎不影响实际生成能力，却可以实现大幅的推理效率提升。</font>**

:::color5
**<font style="color:#601BDE;">8.推理效率 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/webp/29769680/1745760363116-80154b33-2e6b-420f-a9b1-9ab80a7e4a6e.webp)

<font style="color:rgb(136, 136, 136);">▲ 表4：Dynamic-LLaVA-13B 推理效率实测。其中，2K/4K 表示输出的文本 token 数，所有结果均在一张 A100（80G）上测试得出，batch size 固定为8。“×”表示 GPU 显存耗尽</font>

在表 4 中，我们压测了多模态大模型实际推理的时间和 GPU 显存占用。

Dynamic-LLaVA 实现了更快的推理速度和更低的显存占用。FastV 这种对预填充阶段的视觉 token 进行剪枝的方法，随着输出长度的增长，推理效率也逐渐降低。而我们提出的 Dynamic-LLaVA，随着输出变长，相比于 FastV 的推理效率优势也逐渐显现出来。

:::color5
**<font style="color:#601BDE;">9.总结 </font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(63, 63, 63);">针对当前多模态大模型推理效率受限的问题，团队通过分析多模态大模型推理过程中的不同阶段，针对性的设计了推理加速方案。提出了 Dynamic-LLaVA ——第一个同时稀疏化视觉和语言上下文的多模态大模型推理加速框架，将不同推理模式的推理效率优化集成到统一框架中。</font>

<font style="color:rgb(63, 63, 63);">随着多模态大模型技术的发展，尤其是其在复杂推理、长思维链领域的不断进步。我们有理由相信，Dynamic-LLaVA 的应用场景正变得更加广泛，其对输出文本 token 进行稀疏化的模式，会在当前的更长输出、更复杂推理的场景下，体现出更明显的推理加速优势。</font>

# 多模态模型
## CLIP
:::color3
**<font style="color:rgb(51, 51, 51);">核心思想：</font>**

<font style="color:rgb(51, 51, 51);">通过对比学习将不同模态（如图像-文本）映射到同一潜在空间，使匹配的样本对距离更近，不匹配的更远。CLIP的核心公式：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735486640-ffd361d0-724d-4b70-bb6f-25f479fe15cf.png)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740735548727-251dbecf-fe08-4e85-a1ce-6509358d36bf.png)

:::color5
**<font style="color:#601BDE;">1.CLIP架构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">双编码器结构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像编码器（ViT/ResNet）</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器（Transformer）</font>
2. **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：将不同模态的特征映射到同一空间</font>
3. **<font style="color:rgb(51, 51, 51);">对比目标</font>**<font style="color:rgb(51, 51, 51);">：最大化正样本对的相似度，最小化负样本对</font>

:::color5
**<font style="color:#601BDE;">2.训练步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据预处理</font>**
    - <font style="color:rgb(51, 51, 51);">图像：Resize到224x224，随机裁剪/翻转</font>
    - <font style="color:rgb(51, 51, 51);">文本：截断/填充到固定长度（CLIP使用76 tokens）</font>
2. **<font style="color:rgb(51, 51, 51);">特征提取</font>**

```python
# 伪代码示例
image_features = image_encoder(image_batch)  # [batch_size, emb_dim]
text_features = text_encoder(text_batch)     # [batch_size, emb_dim]
```

3. **<font style="color:rgb(51, 51, 51);">相似度矩阵计算</font>**

```python
# 归一化
image_emb = image_features / image_features.norm(dim=-1, keepdim=True)
text_emb = text_features / text_features.norm(dim=-1, keepdim=True)

# 计算相似度矩阵
logit_scale = nn.Parameter(torch.ones([]) * np.log(1/0.07))
logits_per_image = logit_scale * image_emb @ text_emb.t()  # [N, N]
logits_per_text = logits_per_image.t()                     # [N, N]
```

4. **<font style="color:rgb(51, 51, 51);">对比损失计算</font>**

<font style="color:rgb(51, 51, 51);">使用对称交叉熵损失：</font>

```python
labels = torch.arange(batch_size)  # 对角矩阵表示正样本对

loss_i = F.cross_entropy(logits_per_image, labels)
loss_t = F.cross_entropy(logits_per_text, labels)
total_loss = (loss_i + loss_t)/2
```

:::color5
**<font style="color:#601BDE;">3.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点：</font>**

1. <font style="color:rgb(51, 51, 51);">零样本推理能力</font>
2. <font style="color:rgb(51, 51, 51);">跨模态检索高效</font>
3. <font style="color:rgb(51, 51, 51);">对噪声数据鲁棒性强</font>
4. <font style="color:rgb(51, 51, 51);">无需手工标注（利用自然监督信号）</font>

**<font style="color:rgb(51, 51, 51);">缺点：</font>**

1. <font style="color:rgb(51, 51, 51);">需要超大规模数据（CLIP训练用了4亿对）</font>
2. <font style="color:rgb(51, 51, 51);">模态间细粒度对齐困难</font>
3. <font style="color:rgb(51, 51, 51);">计算成本极高（CLIP训练需592 V100 days）</font>
4. <font style="color:rgb(51, 51, 51);">文本描述歧义性问题</font>

:::color5
**<font style="color:#601BDE;">4.应用场景</font>**

:::

| **场景** | **典型应用** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">零样本分类</font> | <font style="color:rgb(51, 51, 51);">ImageNet分类无需训练</font> |
| <font style="color:rgb(51, 51, 51);">跨模态检索</font> | <font style="color:rgb(51, 51, 51);">图文互搜（如Google Images）</font> |
| <font style="color:rgb(51, 51, 51);">生成模型引导</font> | <font style="color:rgb(51, 51, 51);">DALL-E、Stable Diffusion的文本条件生成</font> |
| <font style="color:rgb(51, 51, 51);">视频理解</font> | <font style="color:rgb(51, 51, 51);">视频-文本对齐（如VideoCLIP）</font> |
| <font style="color:rgb(51, 51, 51);">多模态推理</font> | <font style="color:rgb(51, 51, 51);">Visual Question Answering</font> |


:::color5
**<font style="color:#601BDE;">5.改进方法</font>**

:::

1. **训练效率优化**：
    - <font style="color:rgb(51, 51, 51);">FLIP（随机mask图像块加速训练）</font>
    - <font style="color:rgb(51, 51, 51);">DeCLIP（数据增强+动量蒸馏）</font>
2. **对齐增强**：
    - <font style="color:rgb(51, 51, 51);">ALIGN：使用噪声更大的网页数据</font>
    - <font style="color:rgb(51, 51, 51);">FILIP：细粒度token级对比</font>
3. **架构改进**：
    - <font style="color:rgb(51, 51, 51);">BLIP：引入跨模态注意力</font>
    - <font style="color:rgb(51, 51, 51);">FLAVA：统一多模态编码器</font>
4. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">CoOp：可学习的prompt模板</font>
    - <font style="color:rgb(51, 51, 51);">SLIP：结合自监督学习损失</font>

:::color5
**<font style="color:#601BDE;">6.实现代码示例</font>**

:::

```python
# 典型CLIP训练配置
batch_size = 32768    # 需超大显存
learning_rate = 5e-5  # 使用学习率warmup
epochs = 32           # 实际需要更多epoch
temperature = 0.07    # logit缩放因子

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from torchvision.models import vit_b_16  # Using a pre-trained ViT model

class SimpleTokenizer(nn.Module):
    # 这里是一个简化的tokenizer
    def __init__(self, vocab_size, embed_dim):
        super(SimpleTokenizer, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embed_dim)

    def forward(self, input_ids):
        return self.embeddings(input_ids)  # 返回词嵌入

class CLIP(nn.Module):
    def __init__(self, vocab_size, embed_dim, image_size):
        super(CLIP, self).__init__()
        self.visual_encoder = vit_b_16(pretrained=True)  # 使用预训练的ViT模型
        self.visual_encoder.heads = nn.Identity()  # 去掉头部以只保留特征层
        self.tokenizer = SimpleTokenizer(vocab_size, embed_dim)
        self.text_projection = nn.Linear(embed_dim, embed_dim)  # 用于将文本嵌入映射到相同维度

    def encode_image(self, image):
        # 图像编码
        with torch.no_grad():
            features = self.visual_encoder(image)  # 输出维度 (B, embed_dim)
        return features

    def encode_text(self, text):
        # 文本编码
        text_embeddings = self.tokenizer(text)  # 输出维度 (B, seq_len, embed_dim)
        text_embeddings = text_embeddings.mean(dim=1)  # 取平均，输出维度 (B, embed_dim)
        return self.text_projection(text_embeddings)  # 投影到图片特征空间

    def forward(self, images, texts):
        image_features = self.encode_image(images)
        text_features = self.encode_text(texts)
        
        # 归一化特征
        image_features = F.normalize(image_features, dim=-1)
        text_features = F.normalize(text_features, dim=-1)
        
        # 计算点积相似度
        logits = image_features @ text_features.t()  # 输出维度 (B, B)
        return logits

# 维度说明：
# images: (B, 3, 224, 224) -> B是批量大小，3是通道数，224x224是图像大小
# texts: (B, seq_len) -> seq_len是文本序列长度
# 训练伪代码
model = CLIP()
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for images, texts in dataloader:
    logits = model(images, texts)
    labels = torch.arange(len(images))
    loss = F.cross_entropy(logits, labels) + F.cross_entropy(logits.t(), labels)
    loss.backward()
    optimizer.step()
```

### <font style="color:rgb(51, 51, 51);">InfoNCE</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">InfoNCE是一种基于噪声对比估计的损失函数，用于最大化正样本对的互信息（Mutual Information）。其公式为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740712765539-f4f8df7c-e753-44e7-af4b-4d48c28958fc.png)

+ _<font style="color:rgb(51, 51, 51);">z</font>_<sub>_<font style="color:rgb(51, 51, 51);">i</font>_</sub><font style="color:rgb(51, 51, 51);">：锚点样本（anchor）的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">j</font></sub><sup><font style="color:rgb(51, 51, 51);">+</font></sup><font style="color:rgb(51, 51, 51);">：正样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">z</font><sub><font style="color:rgb(51, 51, 51);">k</font></sub><sup><font style="color:rgb(51, 51, 51);">−</font></sup><font style="color:rgb(51, 51, 51);">：负样本的特征。</font>
+ <font style="color:rgb(51, 51, 51);">s(⋅)：相似度函数（如余弦相似度）。</font>
+ <font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：温度系数（控制分布尖锐程度）。</font>
+ <font style="color:rgb(51, 51, 51);">N</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">：负样本数量。</font>

:::

<font style="color:rgb(51, 51, 51);">对比学习通过构建正负样本对的对比任务，结合InfoNCE损失函数，已成为自监督学习中的核心方法，并在多个领域展现出强大的特征学习能力。</font>

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：一批样本 X={x1,x2,...,xB}。</font>
2. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：对每个样本生成两个增强视图 x</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,x</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">。</font>
3. **<font style="color:rgb(51, 51, 51);">特征提取</font>**<font style="color:rgb(51, 51, 51);">：通过编码器得到特征</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740712844605-72ef504c-26c5-4149-8376-97cf871aae00.png)<font style="color:rgb(51, 51, 51);">。</font>
4. **<font style="color:rgb(51, 51, 51);">相似度计算</font>**<font style="color:rgb(51, 51, 51);">：对每个锚点特征</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">z</font><font style="color:rgb(51, 51, 51);">i</font><font style="color:rgb(51, 51, 51);">a</font>_<font style="color:rgb(51, 51, 51);">z</font>__<font style="color:rgb(51, 51, 51);">i</font>__<font style="color:rgb(51, 51, 51);">a</font>_<font style="color:rgb(51, 51, 51);">，计算：</font>
    - <font style="color:rgb(51, 51, 51);">正样本相似度：s(z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">)</font>
    - <font style="color:rgb(51, 51, 51);">负样本相似度：s(z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">a</font></sup><font style="color:rgb(51, 51, 51);">,z</font><sub><font style="color:rgb(51, 51, 51);">i</font></sub><sup><font style="color:rgb(51, 51, 51);">b</font></sup><font style="color:rgb(51, 51, 51);">), j≠i</font>
5. **<font style="color:rgb(51, 51, 51);">损失计算</font>**<font style="color:rgb(51, 51, 51);">：应用InfoNCE公式，对所有样本求平均损失。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**

+ **<font style="color:rgb(51, 51, 51);">无需标签数据</font>**<font style="color:rgb(51, 51, 51);">：完全自监督学习。</font>
+ **<font style="color:rgb(51, 51, 51);">特征解耦性好</font>**<font style="color:rgb(51, 51, 51);">：学习到对下游任务泛化的特征。</font>
+ **<font style="color:rgb(51, 51, 51);">灵活性高</font>**<font style="color:rgb(51, 51, 51);">：适用于图像、文本、语音等多模态数据。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**

+ **<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">：负样本数量直接影响计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">对数据增强敏感</font>**<font style="color:rgb(51, 51, 51);">：依赖高质量的数据增强策略。</font>
+ **<font style="color:rgb(51, 51, 51);">样本选择偏差</font>**<font style="color:rgb(51, 51, 51);">：负样本可能包含潜在正样本（False Negative）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| **领域** | **应用案例** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">计算机视觉</font>** | <font style="color:rgb(51, 51, 51);">图像分类、目标检测（如SimCLR、MoCo）</font> |
| **<font style="color:rgb(51, 51, 51);">自然语言处理</font>** | <font style="color:rgb(51, 51, 51);">文本相似度计算、句子嵌入（如SimCSE）</font> |
| **<font style="color:rgb(51, 51, 51);">语音处理</font>** | <font style="color:rgb(51, 51, 51);">说话人识别、语音表示学习</font> |
| **<font style="color:rgb(51, 51, 51);">跨模态学习</font>** | <font style="color:rgb(51, 51, 51);">图文匹配（如CLIP）</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">负样本优化</font>**
    - **<font style="color:rgb(51, 51, 51);">动量对比（MoCo）</font>**<font style="color:rgb(51, 51, 51);">：维护动态队列存储历史负样本。</font>
    - **<font style="color:rgb(51, 51, 51);">难负样本挖掘</font>**<font style="color:rgb(51, 51, 51);">：筛选与锚点相似度高的负样本。</font>
2. **<font style="color:rgb(51, 51, 51);">损失函数改进</font>**
    - **<font style="color:rgb(51, 51, 51);">NT-Xent（Normalized Temperature-scaled Cross Entropy）</font>**<font style="color:rgb(51, 51, 51);">：引入归一化和温度参数（SimCLR）。</font>
    - **<font style="color:rgb(51, 51, 51);">Triplet Loss</font>**<font style="color:rgb(51, 51, 51);">：基于锚点-正样本-负样本的三元组损失。</font>
3. **<font style="color:rgb(51, 51, 51);">架构改进</font>**
    - **<font style="color:rgb(51, 51, 51);">不对称编码器</font>**<font style="color:rgb(51, 51, 51);">：使用不同参数的编码器处理正负样本（如BYOL）。</font>
    - **<font style="color:rgb(51, 51, 51);">投影头（Projection Head）</font>**<font style="color:rgb(51, 51, 51);">：在编码器后增加MLP层映射到子空间。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ContrastiveLoss(nn.Module):
    def __init__(self, temperature=0.5):
        super().__init__()
        self.temperature = temperature

    def forward(self, features):
        # features: [2*N, D]（前N个为锚点，后N个为正样本）
        batch_size = features.shape[0] // 2
        labels = torch.cat([torch.arange(batch_size) for _ in range(2)], dim=0)
        labels = (labels.unsqueeze(0) == labels.unsqueeze(1)).float().to(features.device)
        
        # 计算相似度矩阵
        similarity_matrix = F.cosine_similarity(features.unsqueeze(1), features.unsqueeze(0), dim=-1)
        
        # 排除对角线（自身相似度）
        mask = torch.eye(labels.shape[0], dtype=torch.bool).to(features.device)
        labels = labels[~mask].view(labels.shape[0], -1)
        similarity_matrix = similarity_matrix[~mask].view(similarity_matrix.shape[0], -1)
        
        # 选取正样本和负样本
        positives = similarity_matrix[labels.bool()].view(labels.shape[0], -1)
        negatives = similarity_matrix[~labels.bool()].view(similarity_matrix.shape[0], -1)
        
        # 计算InfoNCE损失
        logits = torch.cat([positives, negatives], dim=1)
        labels = torch.zeros(logits.shape[0], dtype=torch.long).to(features.device)
        logits = logits / self.temperature
        loss = F.cross_entropy(logits, labels)
        return loss

# 使用示例
encoder = nn.Linear(2048, 128)  # 假设输入维度2048，输出维度128
projector = nn.Sequential(nn.Linear(128, 256), nn.ReLU(), nn.Linear(256, 128))

x = torch.randn(64, 2048)  # 输入数据（batch_size=32，每个样本生成两个视图）
features = encoder(x)
features = projector(features)
loss_fn = ContrastiveLoss(temperature=0.5)
loss = loss_fn(features)
print(loss.item())

```



### LLAVA与CLIP对齐的对比
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">CLIP</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐 是其核心能力，通过</font>**<font style="color:#ED740C;">对比学习（Contrastive Learning）</font>**<font style="color:rgb(25, 27, 31);">将图像和文本映射到统一的语义空间。</font>

**<font style="color:rgb(25, 27, 31);">LLaVA</font>**<font style="color:rgb(25, 27, 31);"> ：跨模态对齐的核心是通过一个</font>**<font style="color:#ED740C;">轻量级线性投影层将视觉特征映射到语言模型的词嵌入空间</font>**<font style="color:rgb(25, 27, 31);">，结合两阶段训练策略实现高效对齐。以下是详细的技术分解：</font>

**<font style="color:rgb(51, 51, 51);">参考</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://zhuanlan.zhihu.com/p/27728623876](https://zhuanlan.zhihu.com/p/27728623876)

:::

:::color5
**<font style="color:#601BDE;">1.CLIP多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849995591-667a0c79-beab-443f-931c-f351159cd7c4.png)

1. 模型结构
    - <font style="color:rgb(25, 27, 31);">图像编码器：例如 Vision Transformer（ViT）或 ResNet，将图像编码为特征向量。</font>
    - <font style="color:rgb(25, 27, 31);">文本编码器：例如 Transformer，将文本编码为特征向量。</font>
2. 对齐方法
    - <font style="color:rgb(25, 27, 31);">输入：</font>
        * <font style="color:rgb(25, 27, 31);">图像：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[img_1, img_2, ..., img_N]</font>`
        * <font style="color:rgb(25, 27, 31);">文本：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[text_1, text_2, ..., text_N]</font>`
    - <font style="color:rgb(25, 27, 31);">步骤：</font>
        * **<font style="color:rgb(25, 27, 31);">a.特征提取：</font>**
            + <font style="color:rgb(25, 27, 31);">图像特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">I = image_encoder(img_1), ..., image_encoder(img_N)</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">→ 维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
            + <font style="color:rgb(25, 27, 31);">文本特征：</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">T = text_encoder(text_1), ..., text_encoder(text_N)</font>`<font style="color:rgb(25, 27, 31);"> → 维度 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, d]</font>`
        * **<font style="color:rgb(25, 27, 31);">b.相似度计算：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">计算所有图像和文本的余弦相似度矩阵</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S</font>`<font style="color:rgb(25, 27, 31);">，维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[N, N]</font>`<font style="color:rgb(25, 27, 31);">：</font>

```plain
S[i][j] = cosine_similarity(I[i], T[j])
```

    - <font style="color:rgb(25, 27, 31);">理想情况下，对角线元素 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">S[i][i]</font>`<font style="color:rgb(25, 27, 31);"> 应最大（匹配对），非对角线元素应较小（不匹配对）</font>
        * **<font style="color:rgb(25, 27, 31);">c.对比损失（InfoNCE）：</font>**<font style="color:rgb(25, 27, 31);"></font>
            + <font style="color:rgb(25, 27, 31);">对每个图像</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">i</font>`<font style="color:rgb(25, 27, 31);">，计算其与所有文本的相似度，通过 softmax 得到概率分布：</font>

```plain
p_image2text(i) = exp(S[i][i]/τ) / sum_{j=1}^N exp(S[i][j]/τ)
```

        * <font style="color:rgb(25, 27, 31);">对每个文本</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">j</font>`<font style="color:rgb(25, 27, 31);">，同理计算</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">p_text2image(j)</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">总损失为两个方向的交叉熵之和：</font>
        * <font style="color:rgb(25, 27, 31);">其中 τ 是温度参数，控制分布集中程度。</font>

```plain
loss = -1/(2N) * sum_{i=1}^N [log(p_image2text(i)) + log(p_text2image(i))]
```

:::color5
**<font style="color:#601BDE;">2.LLAVA多模态对齐</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741849977575-d145922b-3207-4c22-a51a-e5519ce67e37.png)

1. **模型架构**
    1. <font style="color:rgb(25, 27, 31);">视觉编码器：CLIP-ViT-L/14（输出维度</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[H, W, D_img] = [16, 16, 1024]</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    2. <font style="color:rgb(25, 27, 31);">线性投影层（对齐模块）：单层全连接网络（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj ∈ R^{D_img × D_text}</font>`<font style="color:rgb(25, 27, 31);">），将图像特征转换为语言模型兼容的维度（如</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text=4096</font>`<font style="color:rgb(25, 27, 31);">）。</font>
    3. <font style="color:rgb(25, 27, 31);">语言模型：</font>[<font style="color:rgb(9, 64, 142);">Vicuna</font>](https://zhida.zhihu.com/search?content_id=254568449&content_type=Article&match_order=1&q=Vicuna&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（LLaMA架构的指令微调版本），词嵌入维度为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">D_text</font>`<font style="color:rgb(25, 27, 31);">。</font>
2. **对齐步骤**
    1. **<font style="color:rgb(25, 27, 31);">视觉特征处理</font>**
        * <font style="color:rgb(25, 27, 31);">输入图像：尺寸</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">224×224</font>`<font style="color:rgb(25, 27, 31);">，通过ViT划分为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">16×16</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">个patch，输出特征图</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">[16×16, 1024]</font>`<font style="color:rgb(25, 27, 31);">。</font>
        * <font style="color:rgb(25, 27, 31);">特征扁平化：将空间维度合并为序列，得到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×1024</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的特征矩阵。</font>
        * <font style="color:rgb(25, 27, 31);">线性投影：通过 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">W_proj</font>`<font style="color:rgb(25, 27, 31);"> 将每个patch特征转换为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">4096</font>`<font style="color:rgb(25, 27, 31);"> 维，得到 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);"> 的视觉token序列。</font>
    2. **<font style="color:rgb(25, 27, 31);">步骤2：与文本token拼接</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">将视觉token（</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">256×4096</font>`<font style="color:rgb(25, 27, 31);">）与文本token（如问题“描述这张图片”）拼接，形成联合输入序列。</font>
        * <font style="color:rgb(25, 27, 31);">示例：输入序列 = [IMG_1, IMG_2, ..., IMG_256] + [Q1, Q2, ..., Qn]</font>
        * <font style="color:rgb(25, 27, 31);">语言模型（Vicuna）将此序列视为“多模态prompt”，自回归生成答案。</font>
    3. **<font style="color:rgb(25, 27, 31);">预训练（特征对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：对齐视觉与语言特征，使投影后的视觉token能被语言模型“理解”。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用约 600K 图像-文本对（来自CC3M等），构造单轮指令数据（如“请描述图像” + 人工标注描述）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">冻结参数：</font>**<font style="color:#ED740C;">视觉编码器和语言模型权重固定</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">仅训练投影层：通过最小化语言模型的交叉熵损失，优化视觉到文本的映射。</font>
            + <font style="color:rgb(25, 27, 31);">关键公式：</font>
    4. **<font style="color:rgb(25, 27, 31);">阶段2：指令微调（任务对齐）</font>**<font style="color:rgb(25, 27, 31);"></font>
        * <font style="color:rgb(25, 27, 31);">目标：提升模型对复杂指令（如推理、问答）的响应能力。</font>
        * <font style="color:rgb(25, 27, 31);">数据：使用158K GPT-4生成的指令-答案对（涵盖描述、推理、对话等任务）。</font>
        * <font style="color:rgb(25, 27, 31);">训练细节：</font>
            + <font style="color:rgb(25, 27, 31);">解冻语言模型：</font>**<font style="color:#ED740C;">微调语言模型参数（LoRA或全参数微调）</font>**<font style="color:rgb(25, 27, 31);">。</font>
            + <font style="color:rgb(25, 27, 31);">联合优化：投影层和语言模型共同更新，强化跨模态交互。</font>
            + <font style="color:rgb(25, 27, 31);">示例任务：</font>
                - <font style="color:rgb(25, 27, 31);">输入：图像 + “图中的小狗是什么颜色？”</font>
                - <font style="color:rgb(25, 27, 31);">输出：语言模型需结合视觉token（如“黑色毛发”）生成答案“黑色”。</font>

## <font style="color:rgb(31, 35, 40);">SigLIP</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">SigLIP（</font>**<font style="color:rgb(51, 51, 51);">Sigmoid Loss for Language Image Pre-Training</font>**<font style="color:rgb(51, 51, 51);">）是 Google DeepMind 在 2023 年提出的多模态对比学习模型，基于经典 CLIP 架构改进。传统 CLIP 采用 Softmax 交叉熵损失，面临</font>**<font style="color:rgb(51, 51, 51);">负样本偏差</font>**<font style="color:rgb(51, 51, 51);">（大量不相关负样本对训练效率的影响）和</font>**<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">（需计算所有负样本对）的问题。SigLIP 通过 </font>**<font style="color:rgb(51, 51, 51);">Sigmoid 损失函数</font>**<font style="color:rgb(51, 51, 51);">和创新负采样策略，显著提升了训练效率和模型性能。</font>

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **损失函数改进**：
    - <font style="color:rgb(51, 51, 51);">将 CLIP 的对称 Softmax 损失替换为</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Sigmoid 损失</font>**<font style="color:rgb(51, 51, 51);">，直接优化正样本对的相似度。</font>
    - <font style="color:rgb(51, 51, 51);">数学形式：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086031060-31ade1c1-d5c3-46b4-bc1a-ed325c425689.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 s</font><sub><font style="color:rgb(51, 51, 51);">ij</font></sub><font style="color:rgb(51, 51, 51);">是图像-文本相似度，τ为温度系数，λ 负样本权重。</font>
2. **动态负采样**：
    - <font style="color:rgb(51, 51, 51);">每个 Batch 中仅采样部分负样本（如 1/4），降低计算量。</font>
    - <font style="color:rgb(51, 51, 51);">采用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Difficulty-aware 采样</font>**<font style="color:rgb(51, 51, 51);">：优先选择与正样本相似度高的困难负样本。</font>
3. **训练效率优化**：
    - <font style="color:rgb(51, 51, 51);">去除 CLIP 的对称损失设计，单模态编码器可独立训练。</font>
    - <font style="color:rgb(51, 51, 51);">支持超大 Batch Size（可达百万级）训练。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Web 级图文对：LAION-2B（SigLIP 专用子集）、ALIGN 的 JFT-3B。</font>
    - <font style="color:rgb(51, 51, 51);">合成数据：通过图像描述生成模型（如 PaLI）增强文本多样性。</font>
+ **<font style="color:rgb(51, 51, 51);">数据清洗</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于 CLIP 相似度过滤低质量样本（阈值保留 Top 30%）。</font>
    - <font style="color:rgb(51, 51, 51);">语言过滤（保留英语、西班牙语等主要语言）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">SigLIP 沿用 CLIP 的双塔架构</font>

**<font style="color:rgb(51, 51, 51);">关键差异</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. **<font style="color:rgb(51, 51, 51);">投影层设计</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">独立可学习温度参数 τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">，非共享权重。</font>
    - <font style="color:rgb(51, 51, 51);">投影层维度可调整（默认 512 维）。</font>
2. **<font style="color:rgb(51, 51, 51);">编码器选择</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像编码器：ViT-G/14（基于 EVA-02 预训练）、ResNet-RS-152。</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器：BERT-style Transformer，最大长度 64。</font>
3. **<font style="color:rgb(51, 51, 51);">高效分块实现：</font>**

**<font style="color:rgb(25, 27, 31);">对比训练通常利用数据并行性</font>**<font style="color:rgb(25, 27, 31);">。当数据分布在D个设备上时计算损失，需要收集所有嵌入，这涉及到昂贵的全收集操作(</font>**<font style="color:rgb(25, 27, 31);">all-gathers</font>**<font style="color:rgb(25, 27, 31);">)，更重要的是，</font>**<font style="color:rgb(25, 27, 31);">需要实例化一个内存密集型的</font>**<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">|B|×|B|</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">两两相似度矩阵</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">然而，</font>**<font style="color:rgb(25, 27, 31);">Sigmoid损失特别适合于一种内存高效、快速且数值稳定的实现方式，</font>****<font style="color:#74B602;">这种方式改善了上述两个问题。将每个设备上的批量大小表示为 </font>**<font style="color:#74B602;">b=|B|/D</font><font style="color:rgb(25, 27, 31);"> ，损失可以重新表述为：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086494587-891d2071-1a7e-44c5-b43b-e9dd721f728f.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086480464-f79f2096-17bc-4dcd-9f37-78d018a282ac.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练初始化**：
    - <font style="color:rgb(51, 51, 51);">图像编码器：加载 EVA-02 或 ResNet 预训练权重。</font>
    - <font style="color:rgb(51, 51, 51);">文本编码器：随机初始化或加载 BERT 权重。</font>
2. **对比学习训练**：
    - **<font style="color:rgb(51, 51, 51);">输入构造</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">Batch 内图像-文本对：正样本为匹配对，负样本来自同 Batch 其他样本。</font>
        * <font style="color:rgb(51, 51, 51);">动态采样 25% 负样本参与损失计算。</font>
    - **<font style="color:rgb(51, 51, 51);">损失计算</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">计算所有正样本对的 Sigmoid 概率。</font>
        * <font style="color:rgb(51, 51, 51);">仅对采样的负样本计算 1−σ(s</font><sub><font style="color:rgb(51, 51, 51);">ij</font></sub><font style="color:rgb(51, 51, 51);">)。</font>
    - **<font style="color:rgb(51, 51, 51);">梯度更新</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">采用 LAMB 优化器，支持超大 Batch（可达 1M）。</font>
        * <font style="color:rgb(51, 51, 51);">学习率 warmup 至 1e-3，余弦衰减调度。</font>
3. **微调阶段（可选）**：
    - <font style="color:rgb(51, 51, 51);">冻结图像编码器，仅微调文本编码器适配下游任务。</font>
    - <font style="color:rgb(51, 51, 51);">添加任务特定头部（如分类层）。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">训练效率提升：相比 CLIP，达到相同性能需 1/10 计算量。</font>
2. <font style="color:rgb(51, 51, 51);">更优的零样本性能：在 ImageNet 零样本分类上超越 CLIP 5%~10%。</font>
3. <font style="color:rgb(51, 51, 51);">支持超大 Batch Size：适合分布式训练。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">对温度参数</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">敏感，需精细调参。</font>
2. <font style="color:rgb(51, 51, 51);">文本多样性受限：依赖预训练文本编码器的能力。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">零样本图像分类</font>**<font style="color:rgb(51, 51, 51);">：直接匹配文本标签特征。</font>
2. **<font style="color:rgb(51, 51, 51);">跨模态检索</font>**<font style="color:rgb(51, 51, 51);">：图文互搜（如 Google Images 搜索）。</font>
3. **<font style="color:rgb(51, 51, 51);">多模态内容审核</font>**<font style="color:rgb(51, 51, 51);">：识别图文不一致的违规内容。</font>
4. **<font style="color:rgb(51, 51, 51);">机器人视觉导航</font>**<font style="color:rgb(51, 51, 51);">：结合文本指令理解环境。</font>
5. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：为生成模型（如 Stable Diffusion）提供跨模态对齐信号。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">混合损失函数</font>**<font style="color:rgb(51, 51, 51);">：结合 Sigmoid 损失与 KL 散度损失（对齐分布）。</font>
2. **<font style="color:rgb(51, 51, 51);">多粒度对比</font>**<font style="color:rgb(51, 51, 51);">：引入局部区域-短语对齐（类似 ALBEF）。</font>
3. **<font style="color:rgb(51, 51, 51);">动态温度调整</font>**<font style="color:rgb(51, 51, 51);">：根据训练阶段自动调节</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">τ</font>_<font style="color:rgb(51, 51, 51);">。</font>
4. **<font style="color:rgb(51, 51, 51);">跨模态蒸馏</font>**<font style="color:rgb(51, 51, 51);">：用 SigLIP 指导小型任务模型训练。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SigLIP(nn.Module):
    def __init__(self, image_encoder, text_encoder, proj_dim=512):
        super().__init__()
        self.image_encoder = image_encoder  # 例如 ViT
        self.text_encoder = text_encoder    # 例如 BERT
        self.image_proj = nn.Linear(image_encoder.output_dim, proj_dim)
        self.text_proj = nn.Linear(text_encoder.config.hidden_size, proj_dim)
        self.temperature = nn.Parameter(torch.ones([]) * 0.07)  # 可学习温度参数

    def forward(self, images, texts):
        # 编码图像和文本
        image_feats = self.image_encoder(images)  # (B, D_img)
        text_feats = self.text_encoder(texts.input_ids, attention_mask=texts.attention_mask).last_hidden_state[:,0]  # (B, D_text)
        
        # 投影并归一化
        image_emb = F.normalize(self.image_proj(image_feats), dim=-1)  # (B, D)
        text_emb = F.normalize(self.text_proj(text_feats), dim=-1)     # (B, D)
        
        # 计算相似度矩阵
        logits = image_emb @ text_emb.T  # (B, B)
        logits = logits / self.temperature.exp()
        return logits

def siglip_loss(logits, neg_sample_ratio=0.25):
    batch_size = logits.size(0)
    labels = torch.arange(batch_size, device=logits.device)  # 对角线为正样本
    
    # 正样本损失
    pos_logits = logits.diag().unsqueeze(-1)  # (B,1)
    pos_loss = -F.logsigmoid(pos_logits).mean()
    
    # 负样本采样
    neg_mask = ~torch.eye(batch_size, dtype=torch.bool, device=logits.device)
    neg_logits = logits[neg_mask].view(batch_size, -1)  # (B, B-1)
    
    # 动态选择困难负样本
    k = int(neg_sample_ratio * (batch_size - 1))
    topk_values, _ = torch.topk(neg_logits, k=k, dim=1)
    sampled_neg = topk_values  # (B, k)
    
    # 负样本损失
    neg_loss = -torch.log(1 - torch.sigmoid(sampled_neg)).mean()
    
    return pos_loss + neg_loss

# 使用示例
image_encoder = vit_base_patch16_224(pretrained=True)
text_encoder = BertModel.from_pretrained('bert-base-uncased')
model = SigLIP(image_encoder, text_encoder)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

# 训练循环
for images, texts in dataloader:
    logits = model(images, texts)
    loss = siglip_loss(logits)
    loss.backward()
    optimizer.step()

```



## EVA-CLIP
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：《</font><font style="color:rgb(34, 34, 38);">EVA-CLIP: Improved Training Techniques for CLIP at Scale》</font>

**<font style="color:rgb(51, 51, 51);">CLIP的局限性</font>**<font style="color:rgb(51, 51, 51);">：OpenAI的CLIP模型通过对比学习实现图像-文本对齐，但受限于模型规模（如最大ViT-L/14）和训练效率。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">扩展需求</font>**<font style="color:rgb(51, 51, 51);">：大规模视觉-语言预训练需要更高容量模型，但直接放大CLIP会面临训练不稳定、收敛困难等问题。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">EVA-CLIP目标</font>**<font style="color:rgb(51, 51, 51);">：智源研究院提出EVA-CLIP，通过渐进式扩展策略训练更大模型（如ViT-G/14），突破性能天花板。</font>

:::

<font style="color:rgb(51, 51, 51);">EVA-CLIP通过渐进式扩展和训练策略优化，显著提升了视觉-语言对齐能力，为多模态任务提供了强大的基础模型。其核心创新在于平衡模型规模与训练稳定性，未来可向高效推理和少样本学习方向发展。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741093312252-7dc4f848-6e70-4a81-97b4-4d3042ce32f5.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">渐进式扩展（Evolving Scaling）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">从小模型（ViT-B）开始逐步放大到ViT-G，复用中间参数，稳定训练过程。</font>
    - <font style="color:rgb(51, 51, 51);">避免直接训练超大模型的优化困难。</font>
+ **<font style="color:rgb(51, 51, 51);">锁定图像塔（Locked-image Tuning）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">在预训练后冻结图像编码器，仅微调文本编码器，减少过拟合风险。</font>
+ **<font style="color:rgb(51, 51, 51);">混合分辨率训练</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">动态调整输入图像分辨率（如224x224与336x336交替）提升泛化性。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像-文本对</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">公开数据：LAION-2B、COCO、Visual Genome等。</font>
    - <font style="color:rgb(51, 51, 51);">专有数据：经过清洗的网页爬取数据（约5B对）。</font>
+ **<font style="color:rgb(51, 51, 51);">数据筛选</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于CLIP相似度过滤低质量图文对。</font>
    - <font style="color:rgb(51, 51, 51);">平衡多语言数据（中/英占比约1:3）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">基于ViT架构，最大支持ViT-Giant（ViT-G，宽度1408，层数40）。</font>
    - <font style="color:rgb(51, 51, 51);">引入</font>**<font style="color:rgb(51, 51, 51);">EVA-ViT</font>**<font style="color:rgb(51, 51, 51);">改进：</font>
        * <font style="color:rgb(51, 51, 51);">使用</font>**<font style="color:#74B602;">动态位置编码（Dynamic Position Bias）</font>**<font style="color:rgb(51, 51, 51);">替代固定位置编码。</font>
        * <font style="color:rgb(51, 51, 51);">替换部分FFN层为卷积增强局部感知。</font>
+ **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">Transformer结构（与CLIP相同，12层，宽度512）。</font>
+ **<font style="color:rgb(51, 51, 51);">投影层</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">独立线性层将图像/文本特征映射到共享对比空间（维度：4096）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练阶段**：
    - **<font style="color:rgb(51, 51, 51);">数据</font>**<font style="color:rgb(51, 51, 51);">：4B图像-文本对，混合分辨率输入。</font>
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：对比损失（InfoNCE），最大化匹配对的相似度。</font>
    - **<font style="color:rgb(51, 51, 51);">优化</font>**<font style="color:rgb(51, 51, 51);">：AdamW，学习率预热+余弦衰减，批量大小32K。</font>
2. **锁定微调阶段**：
    - <font style="color:rgb(51, 51, 51);">冻结视觉编码器参数。</font>
    - <font style="color:rgb(51, 51, 51);">仅更新文本编码器和投影层参数。</font>
    - <font style="color:rgb(51, 51, 51);">目标：提升特定任务（如零样本分类）的泛化性。</font>
3. **混合训练策略**：
    - <font style="color:rgb(51, 51, 51);">交替使用不同分辨率输入（如50% 224x224，50% 336x336）。</font>
    - <font style="color:rgb(51, 51, 51);">动态掩码部分图像块以增强鲁棒性。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">性能显著超越CLIP（ViT-G在ImageNet零样本达80.5%）。</font>
+ <font style="color:rgb(51, 51, 51);">渐进式扩展策略稳定，可训练超10B参数模型。</font>
+ <font style="color:rgb(51, 51, 51);">混合分辨率提升跨尺度泛化能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">训练计算成本极高（需数千块GPU）。</font>
+ <font style="color:rgb(51, 51, 51);">依赖海量数据清洗，工程复杂度高。</font>
+ <font style="color:rgb(51, 51, 51);">超大模型推理延迟较高。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">零样本分类</font>**<font style="color:rgb(51, 51, 51);">：直接匹配图像与类别文本描述。</font>
+ **<font style="color:rgb(51, 51, 51);">图文检索</font>**<font style="color:rgb(51, 51, 51);">：跨模态搜索（图搜文/文搜图）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态生成</font>**<font style="color:rgb(51, 51, 51);">：作为图像生成模型（如Stable Diffusion）的编码器。</font>
+ **<font style="color:rgb(51, 51, 51);">细粒度理解</font>**<font style="color:rgb(51, 51, 51);">：结合检测/分割模型提升场景理解。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化部署</font>**<font style="color:rgb(51, 51, 51);">：知识蒸馏到小模型（如ViT-B）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态增强</font>**<font style="color:rgb(51, 51, 51);">：融合音频/视频数据扩展应用边界。</font>
+ **<font style="color:rgb(51, 51, 51);">动态分辨率推理</font>**<font style="color:rgb(51, 51, 51);">：根据输入内容自适应调整分辨率。</font>
+ **<font style="color:rgb(51, 51, 51);">提示学习</font>**<font style="color:rgb(51, 51, 51);">：引入可训练提示（Prompt Tuning）提升少样本能力。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn
from transformers import ViTModel, BertModel

class EVACLIP(nn.Module):
    def __init__(self, vit_model="eva_vit_g", text_model="bert-base"):
        super().__init__()
        # 视觉编码器
        self.visual = ViTModel.from_pretrained(vit_model)
        # 文本编码器
        self.text = BertModel.from_pretrained(text_model)
        # 投影层
        self.visual_proj = nn.Linear(1408, 4096)  # ViT-G隐藏层维度1408
        self.text_proj = nn.Linear(768, 4096)     # BERT-base隐藏层维度768
        
    def forward(self, images, input_ids, attention_mask):
        # 图像特征提取
        vis_features = self.visual(images).last_hidden_state[:, 0, :]  # [CLS] token
        vis_emb = self.visual_proj(vis_features)
        
        # 文本特征提取
        text_features = self.text(input_ids, attention_mask).last_hidden_state[:, 0, :]
        text_emb = self.text_proj(text_features)
        
        # 归一化
        vis_emb = vis_emb / vis_emb.norm(dim=-1, keepdim=True)
        text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
        
        return vis_emb, text_emb

# 对比损失计算
def contrastive_loss(logits, temperature=0.07):
    labels = torch.arange(logits.size(0), device=logits.device)
    loss_i = nn.CrossEntropyLoss()(logits / temperature, labels)
    loss_t = nn.CrossEntropyLoss()(logits.t() / temperature, labels)
    return (loss_i + loss_t) / 2

```

```python
model = EVACLIP()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

for batch in dataloader:
    images, texts = batch
    # 文本编码
    text_inputs = tokenizer(texts, padding=True, return_tensors="pt")
    # 前向计算
    vis_emb, text_emb = model(images, text_inputs.input_ids, text_inputs.attention_mask)
    # 计算相似度矩阵
    logits = vis_emb @ text_emb.t() * torch.exp(torch.tensor(100.0))
    # 损失计算
    loss = contrastive_loss(logits)
    # 反向传播
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

```

## <font style="color:rgb(51, 51, 51);">FLAVA</font>
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">多模态统一需求</font>**<font style="color:rgb(51, 51, 51);">：传统多模态模型（如CLIP、ViLBERT）通常需单独训练单模态编码器，导致跨模态任务与单模态任务性能难以兼顾。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">Meta AI的突破</font>**<font style="color:rgb(51, 51, 51);">：2022年提出的FLAVA旨在构建统一的视觉-语言基础模型，</font>**<font style="color:rgb(51, 51, 51);">同时支持单模态（纯文本/图像）和跨模态任务</font>**<font style="color:rgb(51, 51, 51);">，解决多场景适配问题。</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741159070937-0efc1844-07a0-41e3-9f81-5c26321e9fd5.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">统一架构设计</font>**<font style="color:rgb(51, 51, 51);">：单模态（文本/图像）与多模态共享同一Transformer骨干网络，参数复用率超90%。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务联合预训练</font>**<font style="color:rgb(51, 51, 51);">：同时优化文本MLM、图像MAE、图文对比（ITC）、图文匹配（ITM）等6种损失函数。</font>
+ **<font style="color:rgb(51, 51, 51);">模态解耦与融合</font>**<font style="color:rgb(51, 51, 51);">：支持单模态独立推理（如文本分类）和跨模态联合推理（如VQA）。</font>
+ **<font style="color:rgb(51, 51, 51);">零样本泛化</font>**<font style="color:rgb(51, 51, 51);">：通过prompt tuning适配下游任务，无需微调。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多模态数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图文对：Conceptual Captions（CC3M）、SBU Captions等（共4M对）。</font>
+ **<font style="color:rgb(51, 51, 51);">单模态数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">文本：Wikipedia、BookCorpus（纯文本语料）。</font>
    - <font style="color:rgb(51, 51, 51);">图像：ImageNet-1K（纯图像分类数据）。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">文本：BERT式WordPiece分词（词表30K）。</font>
    - <font style="color:rgb(51, 51, 51);">图像：ViT式分块（224x224→16x16 patches）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741159083598-e81701c6-cef1-4f0e-bb10-bc33519fda20.png)

+ **<font style="color:rgb(51, 51, 51);">单模态编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：12层Transformer（类似BERT），处理文本序列。</font>
    - **<font style="color:rgb(51, 51, 51);">图像编码器</font>**<font style="color:rgb(51, 51, 51);">：12层Vision Transformer（ViT），处理图像块序列。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态编码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">共享参数的12层Transformer，输入为</font>`<font style="color:rgb(51, 51, 51);">[CLS] + 文本emb + [SEP] + 图像emb</font>`<font style="color:rgb(51, 51, 51);">。</font>
+ **<font style="color:rgb(51, 51, 51);">特殊Token</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - `<font style="color:rgb(51, 51, 51);">[CLS]</font>`<font style="color:rgb(51, 51, 51);">：聚合多模态表征，用于分类任务。</font>
    - `<font style="color:rgb(51, 51, 51);">[SEP]</font>`<font style="color:rgb(51, 51, 51);">：分隔文本与图像输入。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **单模态预训练**：
    - <font style="color:rgb(51, 51, 51);">文本：MLM（掩码语言建模），掩码率15%。</font>
    - <font style="color:rgb(51, 51, 51);">图像：MAE（掩码自编码），掩码率75%。</font>
2. **多模态联合训练**：
    - **<font style="color:rgb(51, 51, 51);">对比学习（ITC）</font>**<font style="color:rgb(51, 51, 51);">：图文对相似度最大化，负样本来自同batch。</font>
    - **<font style="color:rgb(51, 51, 51);">匹配任务（ITM）</font>**<font style="color:rgb(51, 51, 51);">：二分类判断图文是否匹配。</font>
    - **<font style="color:rgb(51, 51, 51);">多模态MLM</font>**<font style="color:rgb(51, 51, 51);">：联合掩码文本+图像块，预测被掩内容。</font>
3. **零样本适配**：
    - <font style="color:rgb(51, 51, 51);">使用Prompt模板（如</font>`<font style="color:rgb(51, 51, 51);">"A photo of [CLS]"</font>`<font style="color:rgb(51, 51, 51);">）直接生成分类结果。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">统一的单/多模态处理能力，减少部署成本。</font>
+ <font style="color:rgb(51, 51, 51);">零样本性能显著优于CLIP（ImageNet Acc 72.3% vs 68.3%）。</font>
+ <font style="color:rgb(51, 51, 51);">支持复杂多模态推理（需同时理解图文关系的任务）。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">模型参数量大（350M），训练需数千GPU小时。</font>
+ <font style="color:rgb(51, 51, 51);">图像分块丢失局部细节，细粒度任务（如目标检测）需额外设计。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">跨模态检索</font>**<font style="color:rgb(51, 51, 51);">：图文互搜（电商产品搜索）。</font>
+ **<font style="color:rgb(51, 51, 51);">视觉问答（VQA）</font>**<font style="color:rgb(51, 51, 51);">：医疗报告图文联合分析。</font>
+ **<font style="color:rgb(51, 51, 51);">内容审核</font>**<font style="color:rgb(51, 51, 51);">：检测图文不一致的违规内容。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：自动生成教材插图说明。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化</font>**<font style="color:rgb(51, 51, 51);">：知识蒸馏到小型化模型（如FLAVA-Tiny）。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务增强</font>**<font style="color:rgb(51, 51, 51);">：引入视频模态支持时序理解。</font>
+ **<font style="color:rgb(51, 51, 51);">局部感知</font>**<font style="color:rgb(51, 51, 51);">：融合CNN特征保留图像细节。</font>
+ **<font style="color:rgb(51, 51, 51);">增量学习</font>**<font style="color:rgb(51, 51, 51);">：在不遗忘旧任务的前提下扩展新模态。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import BertModel, ViTModel

class FLAVA(torch.nn.Module):
    def __init__(self):
        super().__init__()
        # 单模态编码器
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        self.image_encoder = ViTModel.from_pretrained('google/vit-base-patch16-224')
        # 多模态编码器（共享参数）
        self.multimodal_encoder = BertModel(self.text_encoder.config)
        # 投影头
        self.text_proj = torch.nn.Linear(768, 256)
        self.image_proj = torch.nn.Linear(768, 256)
        
    def forward(self, text_input, image_input):
        # 单模态编码
        text_emb = self.text_encoder(**text_input).last_hidden_state
        image_emb = self.image_encoder(pixel_values=image_input).last_hidden_state
        # 多模态融合
        multimodal_input = torch.cat([
            text_emb[:, 0:1],  # [CLS]
            text_emb[:, 1:], 
            torch.ones_like(text_emb[:, 0:1]) * 0.1,  # [SEP]
            image_emb
        ], dim=1)
        multimodal_output = self.multimodal_encoder(inputs_embeds=multimodal_input)
        # 对比学习投影
        text_proj = self.text_proj(text_emb[:, 0])
        image_proj = self.image_proj(image_emb[:, 0])
        return {
            "text_emb": text_proj,
            "image_emb": image_proj,
            "multimodal_cls": multimodal_output.last_hidden_state[:, 0]
        }

# 示例调用
model = FLAVA()
text_input = {"input_ids": torch.randint(0, 1000, (1, 32)), "attention_mask": torch.ones(1, 32)}
image_input = torch.randn(1, 3, 224, 224)
outputs = model(text_input, image_input)

```

```python
# 多任务损失计算
def multiview_loss(outputs, labels):
    # 对比损失
    logits = outputs["text_emb"] @ outputs["image_emb"].t() / 0.07
    contrastive_loss = F.cross_entropy(logits, labels)
    # 匹配损失（ITM）
    itm_logits = classifier(outputs["multimodal_cls"])
    itm_loss = F.binary_cross_entropy_with_logits(itm_logits, labels)
    # 总损失
    return contrastive_loss + 0.5 * itm_loss

# 零样本分类示例
def zero_shot_classify(image, class_names):
    text_inputs = [f"A photo of a {name}" for name in class_names]
    text_embs = model.encode_text(tokenize(text_inputs))
    image_emb = model.encode_image(image)
    similarity = image_emb @ text_embs.t()
    return torch.argmax(similarity)

```

## ALBEF
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ALBEF（Align before Fuse）是2021年提出的多模态视觉-语言预训练模型，旨在解决传统方法（如CLIP、ALIGN）中的模态对齐问题。传统模型通过对比学习对齐全局特征，但缺乏</font>**<font style="color:#ED740C;">细粒度语义对齐（如物体-属性关系）</font>**<font style="color:rgb(51, 51, 51);">。ALBEF通过</font>**<font style="color:rgb(51, 51, 51);">先对齐再融合</font>**<font style="color:rgb(51, 51, 51);">的策略，结合</font>**<font style="color:#ED740C;">对比学习与跨模态注意力机制</font>**<font style="color:rgb(51, 51, 51);">，提升多模态理解能力。</font>

:::

<font style="color:rgb(51, 51, 51);">ALBEF通过</font>**<font style="color:#74B602;">多阶段对齐策略和动量蒸馏</font>**<font style="color:rgb(51, 51, 51);">，显著提升了多模态任务的性能。其核心思想“</font>**<font style="color:#74B602;">先对齐再融合</font>**<font style="color:rgb(51, 51, 51);">”为后续模型（如BLIP、CoCa）提供了重要参考。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741072497939-e84345c0-2e45-4388-af59-c34384dd3230.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多阶段对齐策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    1. **<font style="color:rgb(51, 51, 51);">单模态对比学习</font>**<font style="color:rgb(51, 51, 51);">：通过图像-文本对比（ITC）初步对齐全局特征。</font>
    2. **<font style="color:rgb(51, 51, 51);">跨模态融合</font>**<font style="color:rgb(51, 51, 51);">：使用跨模态注意力（cross-attention）捕捉细粒度交互。</font>
    3. **<font style="color:rgb(51, 51, 51);">动量蒸馏</font>**<font style="color:rgb(51, 51, 51);">：通过动量模型生成伪标签，缓解数据噪声问题。</font>
+ **<font style="color:rgb(51, 51, 51);">动量编码器</font>**<font style="color:rgb(51, 51, 51);">：维护一个动量更新的图像/文本编码器，生成更稳定的特征表示，避免训练波动。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">4M图像-文本对</font>**<font style="color:rgb(51, 51, 51);">：来自Conceptual Captions、SBU Captions、COCO、Visual Genome等。</font>
    - **<font style="color:rgb(51, 51, 51);">噪声处理</font>**<font style="color:rgb(51, 51, 51);">：通过动量模型过滤低质量样本。</font>
+ **<font style="color:rgb(51, 51, 51);">下游任务数据</font>**<font style="color:rgb(51, 51, 51);">：图像检索（Flickr30K）、视觉问答（VQA2.0）、视觉推理（NLVR2）等。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

<font style="color:rgb(51, 51, 51);">ALBEF包含三个核心模块：</font>

1. **单模态编码器**：
    - **<font style="color:rgb(51, 51, 51);">图像编码器</font>**<font style="color:rgb(51, 51, 51);">：ViT-B/16（12层Transformer，输出197×768特征）。</font>
    - **<font style="color:rgb(51, 51, 51);">文本编码器</font>**<font style="color:rgb(51, 51, 51);">：BERT-base（12层Transformer，输出[CLS]标记作为全局特征）。</font>
2. **多模态编码器**：
    - <font style="color:rgb(51, 51, 51);">6层Transformer，通过跨模态注意力融合图像（CLS标记）与文本特征。</font>
3. **动量编码器**：
    - <font style="color:rgb(51, 51, 51);">图像/文本编码器的动量版本（EMA更新），用于生成伪标签。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **ITC Loss（图像-文本对比）**：

```python
def itc_loss(image_emb, text_emb, temperature=0.07):
    logits = (image_emb @ text_emb.T) / temperature
    labels = torch.arange(logits.size(0)).to(logits.device)
    loss_i = nn.CrossEntropyLoss()(logits, labels)
    loss_t = nn.CrossEntropyLoss()(logits.T, labels)
    return (loss_i + loss_t) / 2
```

2. **ITM Loss（图像-文本匹配）**：  
多模态编码器输出二分类概率，判断图像-文本是否匹配。
3. **动量蒸馏**：使用动量模型生成软标签计算KL散度损失。

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **优点**：
    - <font style="color:rgb(51, 51, 51);">细粒度对齐：跨模态注意力捕捉物体-属性关系。</font>
    - <font style="color:rgb(51, 51, 51);">抗噪声：动量蒸馏提升对噪声数据的鲁棒性。</font>
    - <font style="color:rgb(51, 51, 51);">高效：对比学习预训练加速收敛。</font>
+ **缺点**：
    - <font style="color:rgb(51, 51, 51);">计算开销大：多模态编码器增加参数量。</font>
    - <font style="color:rgb(51, 51, 51);">依赖预训练数据：数据质量影响模型性能。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像-文本检索</font>**<font style="color:rgb(51, 51, 51);">：双向检索（图搜文/文搜图）。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态推理</font>**<font style="color:rgb(51, 51, 51);">：如NLVR2（判断文本是否描述图像内容）。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化设计</font>**<font style="color:rgb(51, 51, 51);">：替换ViT为Swin Transformer减少计算量。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：引入更强的图像/文本增强策略（如Diffusion生成）。</font>
+ **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：联合训练检索、生成、推理任务。</font>
+ **<font style="color:rgb(51, 51, 51);">知识蒸馏</font>**<font style="color:rgb(51, 51, 51);">：用ALBEF作为教师模型压缩小模型。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import BertModel, ViTModel

class ImageEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.vit = ViTModel.from_pretrained("google/vit-base-patch16-224")

    def forward(self, x):
        return self.vit(x).last_hidden_state[:, 0, :]  # [CLS] token

class TextEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")

    def forward(self, input_ids, attention_mask):
        return self.bert(input_ids, attention_mask).last_hidden_state[:, 0, :]

class MultimodalEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(d_model=768, nhead=12)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=6)

    def forward(self, image_emb, text_emb):
        combined = torch.cat([image_emb.unsqueeze(1), text_emb.unsqueeze(1)], dim=1)
        return self.transformer(combined)

class ALBEF(nn.Module):
    def __init__(self, momentum=0.995):
        super().__init__()
        self.img_encoder = ImageEncoder()
        self.txt_encoder = TextEncoder()
        self.multimodal_encoder = MultimodalEncoder()
        
        # Momentum encoders
        self.img_encoder_m = ImageEncoder()
        self.txt_encoder_m = TextEncoder()
        self._init_momentum_models()
        
    def _init_momentum_models(self):
        for param, param_m in zip(self.img_encoder.parameters(), self.img_encoder_m.parameters()):
            param_m.data.copy_(param.data)
            param_m.requires_grad = False
        # Similarly for text encoder...

    @torch.no_grad()
    def momentum_update(self, momentum=0.995):
        # EMA update for momentum encoders
        for param, param_m in zip(self.img_encoder.parameters(), self.img_encoder_m.parameters()):
            param_m.data = momentum * param_m.data + (1 - momentum) * param.data
        # Similarly for text encoder...

```



## BLIP
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">BLIP（Bootstrapping Language-Image Pre-training）</font>**<font style="color:rgb(51, 51, 51);"> 是 Salesforce Research 在 2022 年提出的视觉-语言预训练模型，旨在解决多模态任务中 </font><font style="color:#ED740C;">理解和生成 的统一性问题</font><font style="color:rgb(51, 51, 51);">。传统模型如 CLIP 仅擅长图文对齐，而生成模型如 DALL-E 缺乏细粒度理解能力。BLIP 通过融合多任务预训练和噪声数据清洗策略，显著提升了跨模态任务的性能。</font>

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>["BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation"](https://arxiv.org/abs/2201.12086)
+ **<font style="color:rgb(51, 51, 51);">官方代码</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/salesforce/BLIP](https://github.com/salesforce/BLIP)

:::

<font style="color:rgb(51, 51, 51);">通过 BLIP，研究者可在一个框架内同时解决</font>**<font style="color:#74B602;">视觉理解与生成任务</font>**<font style="color:rgb(51, 51, 51);">，为多模态 AI 应用提供了高效的基础模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740911608928-6827ba7c-3c3e-4682-9d02-d1c927b522fc.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **多模态混合框架（MED）**  
统一编码器-解码器架构，支持以下三种模式灵活切换：
    - **<font style="color:rgb(51, 51, 51);">单模态编码器</font>**<font style="color:rgb(51, 51, 51);">：提取图像和文本特征。</font>
    - **<font style="color:rgb(51, 51, 51);">图文交叉编码器</font>**<font style="color:rgb(51, 51, 51);">：深度融合多模态信息（用于理解任务）。</font>
    - **<font style="color:rgb(51, 51, 51);">条件解码器</font>**<font style="color:rgb(51, 51, 51);">：基于图像生成文本（用于生成任务）。</font>
2. **噪声数据清洗（Captioning & Filtering）**
    - **<font style="color:rgb(51, 51, 51);">Captioner</font>**<font style="color:rgb(51, 51, 51);">：用预训练模型为噪声图像生成高质量文本描述。</font>
    - **<font style="color:rgb(51, 51, 51);">Filter</font>**<font style="color:rgb(51, 51, 51);">：检测并过滤原始数据中的噪声文本-图像对。</font>
3. **多任务预训练目标**  
联合优化以下三个任务：
    - **<font style="color:rgb(51, 51, 51);">图文对比学习（Image-Text Contrastive, ITC）</font>**<font style="color:rgb(51, 51, 51);">：对齐图像和文本的嵌入空间。</font>
    - **<font style="color:rgb(51, 51, 51);">图文匹配（Image-Text Matching, ITM）</font>**<font style="color:rgb(51, 51, 51);">：判断图文是否匹配（二分类）。</font>
    - **<font style="color:rgb(51, 51, 51);">语言建模（Language Modeling, LM）</font>**<font style="color:rgb(51, 51, 51);">：基于图像生成文本描述。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">来源</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">干净数据：COCO、Visual Genome、Flickr30K 等标注数据集。</font>
    - <font style="color:rgb(51, 51, 51);">噪声数据：从网络爬取的 1.4 亿图文对（如 LAION）。</font>
+ **<font style="color:rgb(51, 51, 51);">处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">使用 BLIP 自身的</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Captioner</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">生成合成字幕，扩展高质量数据。</font>
    - <font style="color:rgb(51, 51, 51);">通过 </font>**<font style="color:rgb(51, 51, 51);">Filter</font>**<font style="color:rgb(51, 51, 51);"> 剔除原始噪声数据中的低质量样本。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1740911955832-74df776a-425f-4b0a-bb01-81ab6f4131ad.png)

<font style="color:rgb(0, 0, 0);">caption-filter目的是提取更干净的训练数据（知识蒸馏），提升模型效果：</font>

    - <font style="color:rgb(0, 0, 0);">step1：用大规模数据集预训练一个 BLIP </font><font style="color:rgb(64, 64, 64);">模型</font>
    - <font style="color:rgb(0, 0, 0);">step2：用人工少量标注单独</font><font style="color:rgb(64, 64, 64);">finetune</font><font style="color:rgb(0, 0, 0);">两个子任务高精度模型</font><font style="color:rgb(64, 64, 64);">：</font><font style="color:rgb(0, 0, 0);">（1）</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(0, 0, 0);">模型（训练只用ITC、ITM损失）（2）</font><font style="color:rgb(64, 64, 64);">Captioner</font><font style="color:rgb(64, 64, 64);">模型</font><font style="color:rgb(0, 0, 0);">（训练只用LM损失）</font>
    - <font style="color:rgb(0, 0, 0);">step3：数据集通过</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">模型清洗，过滤掉其中噪声</font>
    - <font style="color:rgb(0, 0, 0);">step4：图片让</font><font style="color:rgb(64, 64, 64);">Captioner</font><font style="color:rgb(64, 64, 64);">模型</font><font style="color:rgb(0, 0, 0);">做图像文本生成，再用</font><font style="color:rgb(64, 64, 64);">Fliter</font><font style="color:rgb(64, 64, 64);"></font><font style="color:rgb(0, 0, 0);">模型对生成的结果做清洗</font>
    - <font style="color:rgb(0, 0, 0);">step5：用step3+step4得到的新的数据集重新训练 BLIP </font><font style="color:rgb(64, 64, 64);">模型</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">整体架构</font>**

```plain
BLIP 模型结构
├── 图像编码器（Image Encoder）: ViT/BERT 提取视觉特征
├── 文本编码器（Text Encoder）: BERT 提取文本特征
├── 图文交叉编码器（Cross-Encoder）: 多模态交互层（ITM 任务）
└── 条件解码器（Conditional Decoder）: 基于图像的文本生成（LM 任务）
```

2. **<font style="color:rgb(51, 51, 51);">关键组件</font>**
    1. **图像编码器**
        * <font style="color:rgb(51, 51, 51);">使用</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">Vision Transformer（ViT）</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">或</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">ResNet</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">提取图像特征。</font>
        * <font style="color:rgb(51, 51, 51);">输出：</font>`<font style="color:rgb(51, 51, 51);">[batch_size, num_patches, hidden_dim]</font>`
    2. **文本编码器/解码器**
        * <font style="color:rgb(51, 51, 51);">基于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">BERT</font>**<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">架构，共享词嵌入层。</font>
        * <font style="color:rgb(51, 51, 51);">编码器：双向自注意力，输出文本特征。</font>
        * <font style="color:rgb(51, 51, 51);">解码器：因果自注意力（掩码），生成文本。</font>
    3. **多模态交互层**
        * <font style="color:rgb(51, 51, 51);">图像特征作为 Key/Value，文本特征作为 Query，通过交叉注意力融合。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

```python
# 图文对比学习（ITC）
def image_text_contrastive_loss(image_emb, text_emb, temperature=0.07):
    logits = (text_emb @ image_emb.T) / temperature
    labels = torch.arange(logits.size(0)).to(logits.device)
    loss = nn.CrossEntropyLoss()(logits, labels)
    return loss

# 图文匹配（ITM）
def image_text_matching_loss(cross_features, labels):
    logits = nn.Linear(768, 2)(cross_features[:, 0, :])  # [CLS] token
    loss = nn.CrossEntropyLoss()(logits, labels)
    return loss

# 语言建模（LM）
def language_modeling_loss(decoder_output, text_labels):
    logits = nn.Linear(768, vocab_size)(decoder_output)
    loss = nn.CrossEntropyLoss()(logits.view(-1, vocab_size), text_labels.view(-1))
    return loss

```

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 统一理解与生成任务，灵活性高</font> | <font style="color:rgb(51, 51, 51);">1. 模型参数量大，训练成本高</font> |
| <font style="color:rgb(51, 51, 51);">2. 噪声数据清洗提升数据质量</font> | <font style="color:rgb(51, 51, 51);">2. 依赖预训练图像编码器（如 ViT）的性能</font> |
| <font style="color:rgb(51, 51, 51);">3. 在少样本场景下表现优异</font> | <font style="color:rgb(51, 51, 51);">3. 生成文本的多样性和创造性有限</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像描述生成（Image Captioning）</font>**
2. **<font style="color:rgb(51, 51, 51);">视觉问答（Visual Question Answering, VQA）</font>**
3. **<font style="color:rgb(51, 51, 51);">图文检索（Image-Text Retrieval）</font>**
4. **<font style="color:rgb(51, 51, 51);">多模态对话系统（如医疗图像诊断报告生成）</font>**

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">模型轻量化：</font>**<font style="color:rgb(51, 51, 51);">使用蒸馏技术（如 TinyBLIP）压缩模型。</font>
2. **<font style="color:rgb(51, 51, 51);">数据增强：</font>**<font style="color:rgb(51, 51, 51);">结合扩散模型生成合成图像-文本对。</font>
3. **<font style="color:rgb(51, 51, 51);">多任务扩展：</font>**<font style="color:rgb(51, 51, 51);">引入目标检测（如 Region-of-Interest 特征）。</font>
4. **<font style="color:rgb(51, 51, 51);">长文本生成优化：</font>**<font style="color:rgb(51, 51, 51);">结合检索增强生成（RAG）提升生成连贯性。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn
from transformers import BertModel, BertTokenizer, ViTModel

class BLIP(nn.Module):
    def __init__(self, config):
        super().__init__()
        # 图像编码器
        self.image_encoder = ViTModel.from_pretrained("google/vit-base-patch16-224")
        # 文本编码器
        self.text_encoder = BertModel.from_pretrained("bert-base-uncased")
        # 图文交叉编码器
        self.cross_encoder = nn.TransformerEncoderLayer(
            d_model=768, nhead=8, dim_feedforward=3072
        )
        # 条件解码器
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=768, nhead=8), num_layers=6
        )

    def forward(self, image, text):
        # 提取图像特征
        image_features = self.image_encoder(image).last_hidden_state
        # 提取文本特征
        text_features = self.text_encoder(text).last_hidden_state
        # 图文交叉编码（ITM 任务）
        cross_features = self.cross_encoder(
            src=text_features, 
            memory=image_features
        )
        # 生成文本（LM 任务）
        output = self.decoder(
            tgt=text_features, 
            memory=cross_features
        )
        return output

# 示例用法
config = {}
model = BLIP(config)
image = torch.randn(1, 3, 224, 224)  # 假设输入图像
text = torch.randint(0, 10000, (1, 32))  # 假设输入文本
output = model(image, text)
print(output.shape)  # torch.Size([1, 32, 768])

```





## BLIP2
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">BLIP-2（Bootstrapping Language-Image Pre-training）是Salesforce Research于2023年提出的多模态预训练模型，旨在高效融合视觉和语言模型。传统视觉语言模型（如CLIP、ALIGN）依赖端到端训练，计算成本高且难以直接利用大语言模型（LLM）。BLIP2通过冻结预训练视觉和语言模型参数，设计轻量级中间模块（Q-Former）实现模态对齐，显著降低了训练成本。</font>

:::

BLIP2通过创新的**<font style="color:#74B602;">两阶段训练和Q-Former设计</font>**，实现了高效的多模态对齐，成为视觉语言任务的新基准。未来可通过动态查询机制和混合微调策略进一步提升性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741073736253-1ab61f42-c942-4034-8eea-006ad2a4a68d.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **两阶段训练范式**：
    - **<font style="color:rgb(51, 51, 51);">Stage1</font>**<font style="color:rgb(51, 51, 51);">: 学习视觉-语言联合表示（冻结图像编码器）。</font>
    - **<font style="color:rgb(51, 51, 51);">Stage2</font>**<font style="color:rgb(51, 51, 51);">: 学习视觉到语言生成（冻结语言模型）。</font>
2. **Querying Transformer (Q-Former)**：
    - <font style="color:rgb(51, 51, 51);">通过可学习的查询向量（learnable queries）与图像特征交互，提取与文本对齐的视觉特征。</font>
    - <font style="color:rgb(51, 51, 51);">结合交叉注意力机制和自注意力机制，实现跨模态信息融合。</font>
3. **参数高效性**：
    - <font style="color:rgb(51, 51, 51);">冻结预训练模型参数（如ViT、EVA-CLIP、OPT、Flan-T5），仅训练Q-Former（约188M参数），大幅减少计算需求。</font>
4. **多任务预训练**：
    - <font style="color:rgb(51, 51, 51);">图像-文本对比学习（ITC）、图像-文本匹配（ITM）、图像描述生成（Captioning）。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：COCO、Visual Genome (VG)、CC3M、CC12M、SBU、LAION 400M。</font>
+ **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：利用预训练模型生成噪声图像的文本描述（Boot strapping策略）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741073751893-dace8c1a-60b2-4d37-a4f4-87bacaaeb078.png)

1. **图像编码器（冻结）**：
    - <font style="color:rgb(51, 51, 51);">可选ViT、EVA-CLIP等，输出图像特征 Zv∈R</font><sup><font style="color:rgb(51, 51, 51);">Nv×d</font></sup><font style="color:rgb(51, 51, 51);">（Nv为图像块数，d</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">为特征维度）。</font>
2. **Q-Former**：<font style="color:rgb(25, 27, 31);">核心是拿一组</font>**<font style="color:#ECAA04;">预定义好的、可学的、固定数量（M个）的Query tokens</font>**<font style="color:rgb(25, 27, 31);">，通过cross attention层去</font>**<font style="color:#74B602;">融合来自image encoder的image token信息</font>**<font style="color:rgb(25, 27, 31);">。</font>
    - <font style="color:rgb(51, 51, 51);">输入：可学习查询向量 Q∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">，Nq为查询数）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：</font>
        * **<font style="color:rgb(51, 51, 51);">图像-查询交叉注意力</font>**<font style="color:rgb(51, 51, 51);">：Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">与Zv交互。</font>
        * **<font style="color:rgb(51, 51, 51);">文本-查询自注意力</font>**<font style="color:rgb(51, 51, 51);">：将文本标记与Q</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">拼接后通过自注意力层。</font>
    - <font style="color:rgb(51, 51, 51);">输出：与文本对齐的视觉特征 Zq∈R</font><sup><font style="color:rgb(51, 51, 51);">Nq×d</font></sup><font style="color:rgb(51, 51, 51);">。</font>
    - **<font style="color:#74B602;">Q-Former学到了什么：</font>**可视化了MLLM中Q-former训练后的输出，验证了**<font style="color:#ED740C;">Q-former确实是在视觉语义级别的压缩</font>**。下图可视化了MLLM中训练好的Q-former的输出，高亮了每个query token相对于原始图片patch的相关性矩阵。我们可以看到，**<font style="color:#ED740C;">将576 image tokens压缩成64 query tokens，每个query token在负责不同的visual concepts，包括不同的objects、attributes和background等等</font>**。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741864585512-f1209667-aa4c-4ef0-a0d4-ded42d069dc1.png)

3. **语言模型（冻结）**：
    - <font style="color:rgb(51, 51, 51);">可选OPT、Flan-T5等，接收Zq</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">作为视觉前缀（visual prompt）生成文本。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

<font style="color:rgb(51, 51, 51);">BLIP2 的训练分为两个阶段，</font>**<font style="color:rgb(51, 51, 51);">逐步解冻不同模块参数</font>**<font style="color:rgb(51, 51, 51);">以实现高效学习：</font><font style="color:rgb(255, 255, 255);">制</font>

| **阶段** | **目标** | **冻结模块** | **训练模块** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">Stage1</font>** | <font style="color:rgb(51, 51, 51);">视觉-语言表示对齐</font> | <font style="color:rgb(51, 51, 51);">图像编码器、语言模型</font> | <font style="color:rgb(51, 51, 51);">Q-Former</font> |
| **<font style="color:rgb(51, 51, 51);">Stage2</font>** | <font style="color:rgb(51, 51, 51);">视觉到语言的生成能力学习</font> | <font style="color:rgb(51, 51, 51);">图像编码器</font> | <font style="color:rgb(51, 51, 51);">Q-Former + 语言模型（可选）</font> |


**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">Stage1：视觉-语言联合表示学习</font>**

**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：让 Q-Former 学会从图像中提取与文本对齐的特征表示，多任务联合训练，同时使用三种预训练任务，共享 Q-Former 参数：</font>

+ **图像-文本对比学习（Image-Text Contrastive Learning, ITC）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：对比图像特征与文本特征相似度</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074304341-6d649817-383a-478b-b27d-7ab7bad5d899.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 s(I,T)为图像-文本相似度，τ</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 为温度系数</font>

+ **图像-文本匹配（Image-Text Matching, ITM）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：二分类判断图像-文本对是否匹配</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">正样本：原始配对文本</font>
        * <font style="color:rgb(51, 51, 51);">负样本：通过 ITC 相似度选择最难的负样本（Hard Negative Mining）</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：二元交叉熵损失</font>
+ **图像描述生成（Image Captioning）**
    - **<font style="color:rgb(51, 51, 51);">方法</font>**<font style="color:rgb(51, 51, 51);">：以图像特征为条件生成文本描述</font>
    - **<font style="color:rgb(51, 51, 51);">实现</font>**<font style="color:rgb(51, 51, 51);">：使用因果掩码的交叉注意力机制</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：交叉熵损失</font>



**<font style="color:rgb(51, 51, 51);background-color:#D9EAFC;">Stage2：视觉到语言生成学习</font>**

**<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：将视觉特征适配到语言模型的输入空间，实现视觉条件文本生成。</font>

1. **<font style="color:rgb(51, 51, 51);">特征投影</font>**

<font style="color:rgb(51, 51, 51);">通过线性层将 Q-Former 输出的视觉特征 Zq</font>_<font style="color:rgb(51, 51, 51);">Zq</font>_<font style="color:rgb(51, 51, 51);"> 映射到语言模型的输入空间：  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074416797-8395e48e-302f-4c9b-9bd4-dfe863726f81.png)<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">其中 </font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074430494-8000b04a-a5af-4779-b625-26f8d65d0420.png)<font style="color:rgb(51, 51, 51);">为可学习投影矩阵</font>

2. **<font style="color:rgb(51, 51, 51);">生成式预训练</font>**
    - **<font style="color:rgb(51, 51, 51);">输入构造</font>**<font style="color:rgb(51, 51, 51);">：将投影后的视觉特征作为前缀（Visual Prompt）拼接到语言模型输入前</font>
    - **<font style="color:rgb(51, 51, 51);">训练任务</font>**<font style="color:rgb(51, 51, 51);">：基于视觉条件的文本生成（Captioning、VQA 等）</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：标准语言模型的自回归损失  
</font>![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074437873-ff037058-da54-4a67-8e6c-95d6f8f2a84c.png)
3. **<font style="color:rgb(51, 51, 51);">语言模型适配</font>**
    - **<font style="color:rgb(51, 51, 51);">OPT/T5 处理差异</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">对于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">OPT</font>**<font style="color:rgb(51, 51, 51);">（自回归模型）：直接输入视觉前缀</font>
        * <font style="color:rgb(51, 51, 51);">对于</font><font style="color:rgb(51, 51, 51);"> </font>**<font style="color:rgb(51, 51, 51);">T5</font>**<font style="color:rgb(51, 51, 51);">（编码器-解码器）：视觉特征仅输入解码器</font>
    - **<font style="color:rgb(51, 51, 51);">参数冻结策略</font>**<font style="color:rgb(51, 51, 51);">：默认冻结语言模型参数，但支持部分微调（如 LoRA）</font>

  
**<font style="background-color:#D9EAFC;">训练技巧与优化</font>**

1. **Bootstrapping 数据增强**
    - <font style="color:rgb(51, 51, 51);">使用预训练模型（如 BLIP）为噪声图像生成伪文本标签</font>
    - <font style="color:rgb(51, 51, 51);">通过质量过滤（Quality Filtering）保留高置信度样本</font>
2. **混合精度训练**
    - <font style="color:rgb(51, 51, 51);">使用 FP16/混合精度降低显存占用</font>
    - <font style="color:rgb(51, 51, 51);">梯度缩放（Gradient Scaling）防止下溢出</font>
3. **学习率策略**
    - <font style="color:rgb(51, 51, 51);">Stage1 使用余弦衰减调度（Cosine Decay）</font>
    - <font style="color:rgb(51, 51, 51);">Stage2 采用线性 warmup（1% 训练步数）</font>
4. **硬件优化**
    - <font style="color:rgb(51, 51, 51);">ZeRO-2 数据并行（DeepSpeed）</font>
    - <font style="color:rgb(51, 51, 51);">梯度检查点（Gradient Checkpointing）节省显存</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">高效利用预训练模型，避免从头训练。</font>
+ <font style="color:rgb(51, 51, 51);">参数效率高，训练成本仅为传统方法的1/10。</font>
+ <font style="color:rgb(51, 51, 51);">支持多种LLM（OPT、T5、Flan-T5）和视觉编码器。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">依赖预训练模型性能，无法微调视觉/语言模型。</font>
+ <font style="color:rgb(51, 51, 51);">多模态推理能力受限于Q-Former的表示能力。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像描述生成</font>**<font style="color:rgb(51, 51, 51);">（Image Captioning）</font>
2. **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">（VQA）</font>
3. **<font style="color:rgb(51, 51, 51);">多模态对话系统</font>**
4. **<font style="color:rgb(51, 51, 51);">图像检索与文本检索</font>**
5. **<font style="color:rgb(51, 51, 51);">零样本视觉推理</font>**

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">部分参数微调</font>**<font style="color:rgb(51, 51, 51);">：对语言模型或图像编码器进行LoRA等轻量级微调。</font>
2. **<font style="color:rgb(51, 51, 51);">增强Q-Former容量</font>**<font style="color:rgb(51, 51, 51);">：增加层数或查询数量。</font>
3. **<font style="color:rgb(51, 51, 51);">引入更强大的预训练模型</font>**<font style="color:rgb(51, 51, 51);">：如PaLM作为LLM、ViT-G作为图像编码器。</font>
4. **<font style="color:rgb(51, 51, 51);">动态查询调整</font>**<font style="color:rgb(51, 51, 51);">：根据输入动态生成查询向量。</font>

  


:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
class QFormer(nn.Module):
    def __init__(self, num_queries=32, dim=768, num_heads=12):
        super().__init__()
        self.queries = nn.Parameter(torch.randn(num_queries, dim))
        self.cross_attn = nn.MultiheadAttention(dim, num_heads)
        self.self_attn = nn.MultiheadAttention(dim, num_heads)
        
    def forward(self, image_features, text_features):
        # 图像-查询交互
        visual_embeds, _ = self.cross_attn(
            self.queries.unsqueeze(1), 
            image_features.transpose(0, 1), 
            image_features.transpose(0, 1)
        )
        
        # 文本-查询交互
        combined = torch.cat([visual_embeds, text_features.transpose(0, 1)], dim=0)
        output, _ = self.self_attn(combined, combined, combined)
        return output.transpose(0, 1)

```

```python
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Blip2Processor, Blip2ForConditionalGeneration

# 示例：使用HuggingFace预训练模型
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载预训练模型
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
model.to(device)

# 处理输入
image = ...  # PIL Image
questions = ["Describe this image in detail."]

# 生成回答
inputs = processor(images=image, text=questions, return_tensors="pt").to(device, torch.float16)
output_ids = model.generate(**inputs, max_new_tokens=100)
answer = processor.decode(output_ids[0], skip_special_tokens=True)
print(answer)

```

```python
import torch
from torch import nn
from transformers import AutoModel

class BLIP2Trainer(nn.Module):
    def __init__(self, image_encoder, q_former, text_decoder):
        super().__init__()
        self.image_encoder = image_encoder  # 冻结参数
        self.q_former = q_former
        self.text_decoder = text_decoder    # 冻结参数
        
        # 投影层
        self.visual_proj = nn.Linear(q_former.dim, text_decoder.config.hidden_size)
        
    def forward(self, images, text_ids):
        # Stage1 前向
        with torch.no_grad():
            image_features = self.image_encoder(images)  # (B, N, D_img)
            
        # Q-Former 处理
        query_outputs = self.q_former(
            image_features, 
            text_embeds=self.text_decoder.get_input_embeddings()(text_ids)
        )  # (B, N_q, D_q)
        
        # Stage2 投影
        visual_embeds = self.visual_proj(query_outputs)  # (B, N_q, D_lm)
        
        # 语言模型生成
        outputs = self.text_decoder(
            input_ids=text_ids,
            inputs_embeds=visual_embeds,
            attention_mask=...,
        )
        return outputs

# 训练循环示例
model = BLIP2Trainer(...)
optimizer = torch.optim.AdamW(model.q_former.parameters(), lr=1e-4)

for images, texts in dataloader:
    # 计算多任务损失
    itc_loss = compute_itc(image_features, text_embeds)
    itm_loss = compute_itm(image_features, text_embeds)
    cap_loss = model(images, text_ids).loss
    
    total_loss = itc_loss + itm_loss + cap_loss
    total_loss.backward()
    optimizer.step()

```

## INSTRUCT-BLIP
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：多模态模型旨在融合视觉和语言信息，完成跨模态任务（如图像描述、视觉问答等）。BLIP（Bootstrapping Language-Image Pre-training）通过联合训练视觉编码器和文本解码器，显著提升了多模态任务性能。然而，传统模型在</font>**<font style="color:rgb(51, 51, 51);">灵活遵循多样化指令</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">零样本任务泛化</font>**<font style="color:rgb(51, 51, 51);">方面存在局限。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">Instruct-BLIP</font>**<font style="color:rgb(51, 51, 51);"> 应运而生，结合</font>**<font style="color:rgb(51, 51, 51);">指令微调（Instruction Tuning）</font>**<font style="color:rgb(51, 51, 51);"> 技术，赋予模型根据自然语言指令动态调整行为的能力，使其能够处理更广泛的任务（如对话、推理等），无需针对每个任务单独训练。</font>

:::

<font style="color:rgb(0, 0, 0);">基于Blip2模型微调，</font>**<font style="color:#74B602;">把指令加到Q-Former中去，让图片也能看到指令。</font>**

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">指令驱动的多任务学习</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">将不同任务（VQA、图像描述、对话等）统一为“指令-输出”格式，增强模型对任务意图的理解。</font>
2. **<font style="color:rgb(51, 51, 51);">轻量级适配器设计</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">在视觉编码器和文本解码器之间插入</font>**<font style="color:rgb(51, 51, 51);">Q-Former（Query Transformer）</font>**<font style="color:rgb(51, 51, 51);">，仅微调解码器和适配器参数，大幅降低训练成本。</font>
3. **<font style="color:rgb(51, 51, 51);">混合指令数据集构建</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">整合26个公开数据集，通过模板将其转化为指令形式，覆盖多样化任务类型。</font>
4. **<font style="color:rgb(51, 51, 51);">零样本泛化能力</font>**<font style="color:rgb(51, 51, 51);">  
</font><font style="color:rgb(51, 51, 51);">通过指令微调，模型可处理未见过的任务描述，如根据新指令生成特定风格的图像描述。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">来源</font>**<font style="color:rgb(51, 51, 51);">：26个公开数据集，包括：</font>
    - **<font style="color:rgb(51, 51, 51);">VQA类</font>**<font style="color:rgb(51, 51, 51);">：VQA v2、OK-VQA、A-OKVQA</font>
    - **<font style="color:rgb(51, 51, 51);">图像描述类</font>**<font style="color:rgb(51, 51, 51);">：COCO、TextCaps</font>
    - **<font style="color:rgb(51, 51, 51);">视觉推理类</font>**<font style="color:rgb(51, 51, 51);">：NLVR2、ScienceQA</font>
    - **<font style="color:rgb(51, 51, 51);">对话类</font>**<font style="color:rgb(51, 51, 51);">：LLaVA-Instruct</font>
+ **<font style="color:rgb(51, 51, 51);">处理方式</font>**<font style="color:rgb(51, 51, 51);">：将每个样本转换为“</font>**<font style="color:rgb(51, 51, 51);">指令-输入-输出</font>**<font style="color:rgb(51, 51, 51);">”三元组。</font>

```python
示例：
指令：请描述这张图片中人物的动作。
输入：图像 + 文本“图中的人在做什么？”
输出：一个人在骑自行车。
```

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741074129337-897c5c05-f29d-4941-8bd7-664d1e733e93.png)

+ **<font style="color:rgb(51, 51, 51);">视觉编码器</font>**<font style="color:rgb(51, 51, 51);">：ViT（Vision Transformer）或 CLIP-ViT，提取图像特征。</font>
+ **<font style="color:rgb(51, 51, 51);">Q-Former</font>**<font style="color:rgb(51, 51, 51);">（核心创新）：</font>
    - <font style="color:rgb(51, 51, 51);">通过可学习的查询向量（Query Vectors）与图像特征交互，生成与任务相关的视觉特征。</font>
    - <font style="color:rgb(51, 51, 51);">包含跨模态注意力层，融合文本指令与视觉信息。</font>
+ **<font style="color:rgb(51, 51, 51);">文本解码器</font>**<font style="color:rgb(51, 51, 51);">：Flan-T5 或 Vicuna，根据指令生成文本输出。</font>
+ **<font style="color:rgb(51, 51, 51);">参数冻结策略</font>**<font style="color:rgb(51, 51, 51);">：仅训练Q-Former和文本解码器，视觉编码器保持冻结。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">预训练阶段</font>**<font style="color:rgb(51, 51, 51);">（可选）：</font>
    - <font style="color:rgb(51, 51, 51);">使用图像-文本对数据（如COCO）训练视觉编码器和Q-Former，学习基础跨模态对齐。</font>
2. **<font style="color:rgb(51, 51, 51);">指令微调阶段</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：图像 + 文本指令（如“请描述图中场景”）。</font>
    - **<font style="color:rgb(51, 51, 51);">输出</font>**<font style="color:rgb(51, 51, 51);">：目标文本（如“阳光下的海滩上有椰子树”）。</font>
    - **<font style="color:rgb(51, 51, 51);">损失函数</font>**<font style="color:rgb(51, 51, 51);">：标准交叉熵损失，优化生成文本与真实标签的匹配度。</font>
    - **<font style="color:rgb(51, 51, 51);">训练细节</font>**<font style="color:rgb(51, 51, 51);">：</font>
        * <font style="color:rgb(51, 51, 51);">Batch size：128</font>
        * <font style="color:rgb(51, 51, 51);">学习率：1e-5（解码器）、3e-5（Q-Former）</font>
        * <font style="color:rgb(51, 51, 51);">优化器：AdamW</font>
        * <font style="color:rgb(51, 51, 51);">训练周期：3-5 epochs</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">多任务统一框架，减少任务特定设计。</font>
    - <font style="color:rgb(51, 51, 51);">零样本泛化能力强，适应新指令。</font>
    - <font style="color:rgb(51, 51, 51);">训练高效，仅微调部分参数。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">依赖大量指令数据构造。</font>
    - <font style="color:rgb(51, 51, 51);">复杂推理任务（如多步数学推理）性能有限。</font>
    - <font style="color:rgb(51, 51, 51);">图像分辨率固定（如224x224），细节信息可能丢失。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">视觉问答</font>**<font style="color:rgb(51, 51, 51);">：回答关于图像内容的复杂问题。</font>
+ **<font style="color:rgb(51, 51, 51);">教育辅助</font>**<font style="color:rgb(51, 51, 51);">：根据教材插图生成题目解析。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态对话</font>**<font style="color:rgb(51, 51, 51);">：结合图像与文本进行自然对话。</font>
+ **<font style="color:rgb(51, 51, 51);">内容生成</font>**<font style="color:rgb(51, 51, 51);">：根据指令生成营销文案或故事。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：引入更多语言风格的指令模板，提升多样性。</font>
2. **<font style="color:rgb(51, 51, 51);">高分辨率处理</font>**<font style="color:rgb(51, 51, 51);">：采用图像分块策略，保留细节。</font>
3. **<font style="color:rgb(51, 51, 51);">动态参数分配</font>**<font style="color:rgb(51, 51, 51);">：根据任务复杂度调整Q-Former参数量。</font>
4. **<font style="color:rgb(51, 51, 51);">强化学习</font>**<font style="color:rgb(51, 51, 51);">：通过人类反馈（RLHF）优化生成结果。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# 加载预训练模型与处理器
processor = Blip2Processor.from_pretrained("Salesforce/instructblip-flan-t5-xxl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/instructblip-flan-t5-xxl")

# 示例输入
image = Image.open("beach.jpg").convert("RGB")
instruction = "请描述这张图片中的场景。"

# 预处理
inputs = processor(
    images=image,
    text=instruction,
    return_tensors="pt",
    padding="max_length",
    max_length=32
)

# 生成输出
output_ids = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7
)

# 解码结果
result = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
print(result)  # 输出：图片展示了一个阳光明媚的海滩，沙滩上有几棵椰子树...

```





# 多模态embedding
## GME<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：GME基于</font>[Qwen2-VL多模态大语言模型](https://www.baidu.com/s?rsv_dl=re_dqa_generate&sa=re_dqa_generate&wd=Qwen2-VL%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&rsv_pq=bb75632a005e0fef&oq=gme%E6%A8%A1%E5%9E%8B&rsv_t=7b43REBTdYaOxpEANGz3/1ADvYTv4FyOCfdzZxXDOunidQ4ckKFae3dsp/+7rPII/6WX&tn=baiduhome_pg&ie=utf-8)<font style="color:rgb(51, 51, 51);">构建，采用对比学习的方法进行训练。每个训练样本包含一个查询、一个相关候选项及多组无关候选项，覆盖文本、图像及图文组合等多种数据类型。通过指令调优，GME能够适应不同的检索任务，如视觉问答（VQA）等，进一步增强了模型的表征能力‌。</font>

**<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://arxiv.org/pdf/2412.16855](https://arxiv.org/pdf/2412.16855)

:::

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741155842432-05f3427b-e5ee-4c57-8a52-da81eb1cc47d.png)

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">训练数据组成：</font>**

多模态表征学习的一个关键因素是训练数据的组成。由于数据多样性对模型性能的影响尚不清楚，我们比较了**<font style="color:#74B602;">在各种检索场景中，用不同数据组合训练的模型的性能</font>**。具体来说，我们使用了四种类型的训练数据：单模态（包括文→文和图→图）、跨模态（包括文->图和图-文）、融合模态训练数据（包括图文→图文）和结合前三种类型的混合数据集。这些不同的训练数据类型导致得到六个模型。

    1. **<font style="color:rgb(34, 34, 34);">结论：多种模态数据平衡</font>**<font style="color:rgb(34, 34, 34);">：GME的训练数据包括单模态、跨模态和融合模态数据。通过实验，研究团队发现</font>**<font style="color:#74B602;">平衡不同类型模态的数据可以显著提高模型在各种检索场景中的表现</font>**<font style="color:rgb(34, 34, 34);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741157470363-66e384b5-4e8c-43d3-8562-47fdb4173201.png)

2. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">多模态数据合成</font>**<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">：</font>

<font style="color:rgb(34, 34, 34);">GME不仅利用了丰富的单模态和跨模态数据，还通过大模型生成技术，合成了海量的混合模态相关性数据。为了高效合成高质量的融合模态数据，研究团队采用了类似于</font>**<font style="color:#74B602;">Doc2Query</font>**<font style="color:rgb(34, 34, 34);">的策略。具体步骤包括：</font>**<font style="color:#74B602;">文档到查询生成、实体提取和查询重写、图像检索和生成以及数据过滤</font>**<font style="color:rgb(34, 34, 34);">。通过这些步骤，研究团队成功合成了113.5万条高质量的融合模态训练数据，显著增强了模型的训练和性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143953209-ea2bce04-a873-4e55-9668-7a8e56036f81.png)

+ **<font style="color:rgb(34, 34, 34);">方法</font>**<font style="color:rgb(34, 34, 34);">：为了高效地合成高质量数据，同时最大限度地减少人工干预，生成融合模态候选来查询相关性数据，我们采用一种类似于Doc2Query的策略。</font>
+ **<font style="color:rgb(34, 34, 34);">数据处理</font>**<font style="color:rgb(34, 34, 34);">：</font>
    1. **<font style="color:rgb(34, 34, 34);">数据源</font>**<font style="color:rgb(34, 34, 34);">：我们主要从维基百科中提取了这些数据。</font>
    2. **<font style="color:rgb(34, 34, 34);">分类</font>**<font style="color:rgb(34, 34, 34);">：为了增强候选数据的领域多样性，我们采用了领域分类模型,对维基百科进行细粒度分类将数据分为动物和植物等类别。</font>
    3. **<font style="color:rgb(34, 34, 34);">采样</font>**<font style="color:rgb(34, 34, 34);">：我们从这些样本中均匀采样分类置信度得分高于0.5的类别和保留数据，我们获得了313284个候选条目，每个条目都包含文本和图像内容。</font>
+ **<font style="color:rgb(34, 34, 34);">Doc2Query生成</font>**<font style="color:rgb(34, 34, 34);">：将每个候选人的内容</font>**<font style="color:#74B602;">输入到LLM中生成文章的quer</font>**<font style="color:rgb(34, 34, 34);">y。为了确保生成的查询的质量，我们构建了一个</font>使用文本向量检索模型对所有段落内容进行向量索引。然后使用query从该集合中检索相应的段落。如果与query关联的文章不在检索的top20中，**<font style="color:#74B602;">则认为该query由于相关性低被丢弃</font>**。在这一步中，我们丢弃了1.2%的生成的查询总数。这个过程使我们能够构建Text→ImageText的训练数据。
+ **实体提取和query改写**：我们的目标是合成**<font style="color:#74B602;">同时包含文本以及图像的query</font>**（即IT→IT类型）。为了实现这一点，我们利用实体提取，然后对提取的实体进行图像检索，并**<font style="color:#74B602;">生成caption以补充图像query</font>**。具体来说，对于第一步中生成的每个查询q，我们使用使用LLM提取实体并**<font style="color:#74B602;">重写原始查询</font>**。例如，**<font style="color:#ED740C;">query “鸢尾花原产自哪里”被改写为“这个职务原产自哪里?”，同时抽取出实体“鸢尾花”</font>**。然后，**<font style="color:#ED740C;">我们寻找与该实体匹配的图像</font>**，并将其与改写的查询q′以形成最终的**<font style="color:#ED740C;">图文query</font>**。
+ **图像检索和生成**：我们探索了两种获取图像的方法。第一种方法使用谷歌图片搜索API检索与实体匹配的图像，保留top5结果。这个第二种方法涉及使用文生图（**<font style="color:#74B602;">FLUX</font>**），使用LLM生成caption，然后使用caption输入到文生图模型以创建相应的图像。这种方法使我们能够快速有效地获得高质量、多样化的图像。合成的结果也可以组装成IT→IT检索类型数据。
+ **数据过滤**：为了保证合成数据的质量，我们对最终数据集进行过滤。我们观察到FLUX生成的图像模型具有一致的质量，而通过谷歌图像搜索API检索的图像通常包括噪声数据。因此，对于通过谷歌图像搜索获得的图像API，我们使用**<font style="color:#74B602;">CLIP模型来评估图像适应相关性</font>**。相似度<0.2的图片将被过滤。
+ **数据量**：通过上述合成流程，我们生成了1135k个高质量的融合模态训练数据条目（包括T→IT和IT→IT类型）。经过筛选，我们保留了1102k个条目，导致数据丢失率为2.9%。整个过程消耗了600 A100 GPU/hour

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741155784840-ac5bb51d-704f-49a6-8ae3-121774124bf2.png)

**<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">3.hard negative：</font>**

<font style="color:rgb(34, 34, 34);">为了提高对比学习模型的质量和多样性，GME采用了两阶段训练策略：首先使用随机选择的负候选进行初始训练，然后使用初始模型检索每个查询的前K个候选，从中选择非相关候选作为硬负样本进行进一步训练。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143670524-671d48af-bcdf-4bc1-84b7-9041f3da9af2.png)

<font style="color:rgb(34, 34, 34);">GME基于MLLM构建，能够接受图像、文本或图像-文本对作为输入。受先前文本嵌入研究的启发，</font>**<font style="color:#74B602;">GME使用的最后一个hidden_state的最后一个token作为输入（表征）</font>**<font style="color:rgb(34, 34, 34);">。尽管预训练的MLLM具有强大的多模态理解能力，但其原始训练目标并未针对表示学习进行优化。因此，需要进行任务特定的微调（或对齐）以增强模型的表示能力。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">对比学习：(triplet loss, infoNCE loss)</font>**

<font style="color:rgb(34, 34, 34);">在对比学习设置中，每个训练实例包括一个查询q、一个相关候选c和一组不相关的候选{c1−,c2−,…,cK−}。为了适应各种下游检索任务，</font>**<font style="color:#74B602;">GME采用了指令调优方法，为每个检索任务添加定制的指令文本i</font>**<font style="color:rgb(34, 34, 34);">。例如，</font>**<font style="color:#ED740C;">对于视觉问答（VQA）任务，指令可以是：“检索一篇文章，为关于图像的给定查询提供答案”。</font>**<font style="color:rgb(34, 34, 34);">训练中，GME通过最小化相关对的余弦距离，同时最大化不相关对的余弦距离来优化模型。</font>

2. **<font style="background-color:#D9EAFC;">两阶段训练</font>**

目的：负样本样本的质量和多样性对于对比学习效果至关重要

    1. 初始训练：我们首先使用随机采样负样本，得到模型M1。
    2. hard_negative继续训练：基于M1，**<font style="color:#74B602;">基于每个query的topk检索结果，使用其中真实的负样本来训练</font>**。然后，我们使用这些hard_negative进一步训练M1，将其细化为最终模型。这种方法可确保模型学习到**<font style="color:#74B602;">更具挑战性的例子中</font>**，从而增强整体效果。
1. **<font style="color:rgb(34, 34, 34);background-color:#D9EAFC;">损失函数：</font>**

<font style="color:rgb(34, 34, 34);">inforNCE loss，</font>其中τ是温度参数，用于缩放余弦相似度以控制分布的集中度。这种方法确保模型有效地学习区分不同模态中的相关信息和不相关信息，从而增强其在多模态检索任务中的性能。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741156039546-efc7956c-bca2-4a0e-8d74-f92099427db7.png)

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">embedding显著提升复杂query的检索精度。</font>
+ <font style="color:rgb(51, 51, 51);">通过LLM的知识迁移增强小样本学习能力。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">推理速度较慢（需LLM前向计算）。</font>
+ <font style="color:rgb(51, 51, 51);">训练需多阶段协调，资源消耗大。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">跨模态搜索</font>**<font style="color:rgb(51, 51, 51);">：电商（图片搜商品描述）、医疗（报告检索影像）。</font>
+ **<font style="color:rgb(51, 51, 51);">开放域问答</font>**<font style="color:rgb(51, 51, 51);">：结合知识库的多模态问答系统。</font>
+ **<font style="color:rgb(51, 51, 51);">内容安全</font>**<font style="color:rgb(51, 51, 51);">：图文一致性审核。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">轻量化</font>**<font style="color:rgb(51, 51, 51);">：用LoRA微调LLM，减少参数量。</font>
+ **<font style="color:rgb(51, 51, 51);">缓存策略</font>**<font style="color:rgb(51, 51, 51);">：对高频query预生成动态embedding。</font>
+ **<font style="color:rgb(51, 51, 51);">多粒度对齐</font>**<font style="color:rgb(51, 51, 51);">：引入物体检测（如Faster R-CNN）实现区域-词对齐。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from transformers import ViTModel, BertModel, LlamaForCausalLM

class GMEModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 编码器
        self.image_encoder = ViTModel.from_pretrained("google/vit-base-patch16-224")
        self.text_encoder = BertModel.from_pretrained("bert-base-uncased")
        # LLM生成动态embedding
        self.llm = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b")
        # 检索适配器
        self.adapter = nn.Sequential(
            nn.Linear(4096, 1024),  # LLM隐藏层维度→检索空间
            nn.ReLU(),
            nn.LayerNorm(1024)
        )

    def forward(self, image, text):
        # 提取特征
        img_feat = self.image_encoder(image).last_hidden_state.mean(dim=1)  # [B, D_img]
        txt_feat = self.text_encoder(text).last_hidden_state[:, 0, :]       # [B, D_txt]
        
        # 拼接特征输入LLM
        llm_input = torch.cat([img_feat, txt_feat], dim=1)  # [B, D_img+D_txt]
        llm_output = self.llm(inputs_embeds=llm_input.unsqueeze(1)).last_hidden_state  # [B, L, D_llm]
        
        # 生成动态embedding
        dynamic_emb = self.adapter(llm_output[:, -1, :])  # 取最后一个token
        return dynamic_emb

# 对比损失示例
def contrastive_loss(query_emb, target_emb, temperature=0.07):
    sim_matrix = torch.matmul(query_emb, target_emb.T) / temperature
    labels = torch.arange(query_emb.size(0)).to(query_emb.device)
    return nn.CrossEntropyLoss()(sim_matrix, labels)

```



[https://arxiv.org/pdf/2412.16855](https://arxiv.org/pdf/2412.16855)

GME: Improving Universal Multimodal Retrieval by Multimodal LLMs

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735291851222-731a0e4c-c9bb-43a4-bb5d-d68722c95253.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741143670524-671d48af-bcdf-4bc1-84b7-9041f3da9af2.png)

# 视觉embedding
## VIT<font style="color:#D22D8D;"> (by草莓师姐)</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">ViT（Vision Transformer）</font>**<font style="color:rgb(51, 51, 51);"> 是 Google Research 在 2020 年提出的纯 Transformer 架构的视觉模型，首次将 Transformer 成功应用于图像分类任务。传统卷积神经网络（CNN）依赖局部感受野和层次化特征提取，而 ViT 通过全局注意力机制捕捉长距离依赖关系，打破了 CNN 在视觉任务中的垄断地位。</font>

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[《An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale》](https://arxiv.org/abs/2010.11929)
+ **<font style="color:rgb(51, 51, 51);">官方实现</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/google-research/vision_transformer](https://github.com/google-research/vision_transformer)
+ **<font style="color:rgb(51, 51, 51);">预训练模型</font>**<font style="color:rgb(51, 51, 51);">：</font>[Hugging Face Model Hub](https://huggingface.co/models?search=vit)

:::

<font style="color:rgb(51, 51, 51);">ViT 的提出标志着视觉模型从 CNN 到 Transformer 的范式转变，为后续多模态大模型（如 CLIP、DALL·E）奠定了重要基础。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742269490237-74a75fcd-f21f-4c67-8cd9-cd671e9162c5.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742528333258-6dd50375-d2fc-4ee8-8a5f-10a43f60ef38.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

1. **<font style="color:rgb(51, 51, 51);">图像分块（Image Patching）</font>**
    - <font style="color:rgb(51, 51, 51);">将图像分割为固定大小的非重叠块（如 16x16），展平后作为序列输入。</font>
2. **<font style="color:rgb(51, 51, 51);">位置编码（Position Embedding）</font>**
    - <font style="color:rgb(51, 51, 51);">为每个图像块添加可学习的位置编码，保留空间信息。</font>
3. **<font style="color:rgb(51, 51, 51);">纯 Transformer 架构</font>**
    - <font style="color:rgb(51, 51, 51);">移除卷积操作，完全依赖自注意力机制进行特征提取。</font>
4. **<font style="color:rgb(51, 51, 51);">大规模预训练</font>**
    - <font style="color:rgb(51, 51, 51);">在超大规模数据集（如 JFT-300M）上预训练，弥补 Transformer 数据效率低的缺陷。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**<font style="color:#D22D8D;"> (by草莓师姐)</font>

:::

+ **<font style="color:rgb(51, 51, 51);">预训练数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">公开数据集</font>**<font style="color:rgb(51, 51, 51);">：ImageNet-21k（14M 图像，21k 类）、JFT-300M（300M 图像，18k 类），监督学习预训练。</font><font style="color:rgba(0, 0, 0, 0.75);">通过大量的标注数据，模型学习到丰富的视觉特征。</font>
    - **<font style="color:rgb(51, 51, 51);">合成数据</font>**<font style="color:rgb(51, 51, 51);">：部分改进工作引入生成模型（如 Diffusion）扩展数据。</font>
+ **<font style="color:rgb(51, 51, 51);">微调数据</font>**<font style="color:rgb(51, 51, 51);">：任务特定数据集（如 ImageNet-1k、CIFAR）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **Patch Embedding**
    - <font style="color:rgb(51, 51, 51);">输入图像（H×W×C） → 分块（N×P²×C） → 展平为 N×(P²·C) → 线性投影为 D 维向量。</font>
    - <font style="color:rgb(51, 51, 51);">例如：224x224 图像 → 16x16 分块 → 196 个块 → 线性投影为 768 维。</font>
2. **位置编码**
    - <font style="color:rgb(51, 51, 51);">可学习的一维向量，与 Patch Embedding 相加。</font>
    - 在Transformer中，位置编码的作用是为了记忆输入的语序信息。ViT中，同样需要位置编码来记录各图像块之间的位置信息。论文使用的是**<font style="color:#74B602;">1-D的位置编码（绝对位置编码）</font>**，即和Transformer论文中使用的位置编码一致，使用了正弦和余弦函数生成位置编码向量。
    - 为什么不用2D-位置编码：作者使用三种编码方式进行实验：1D,2D,相对位置编码，使用三种位置编码得到的结果几乎一致，证明在此任务上三种编码都可以，我们使用最简单的一种。
    - 作者随后也对一维位置编码的结果进行了可视化，下图中是每一个Patch中各位置的位置编码相似性度量，越接近黄色的位置代表越靠近位置编码的中心位置，可以看到，即使是一维位置编码，同样可以比较好地记录二维信息。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741081553073-0e11e349-093a-4ec5-8d5d-3caf966dfff4.png)

3. **Transformer Encoder**
    - <font style="color:rgb(51, 51, 51);">多头自注意力（Multi-Head Self-Attention） + MLP 块（GELU 激活）。</font>
    - <font style="color:rgb(51, 51, 51);">层归一化（LayerNorm）和残差连接（Residual Connection）。</font>
4. **分类头**
    - <font style="color:rgb(51, 51, 51);">取 [CLS] 标志对应的向量 → MLP → Softmax 输出类别概率。</font>
    - <font style="color:rgb(51, 51, 51);">和Transformer类似的，论文也添加了一个<cls>Token用来代表全局(整个图片)的特征向量，和BERT类似，当我们做图片分类任务时，我们可以使用对这个特征向量进行MLP，得到分类结果，他的形状是1 × 768，我们将其和上述的输入做合并，输入矩阵形状为197 × 768 .</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练（大规模数据）**：
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：图像分类（交叉熵损失）。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdamW，余弦学习率衰减。</font>
    - **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：RandAugment、MixUp、CutMix。</font>
2. **微调（下游任务）**：
    - **<font style="color:rgb(51, 51, 51);">目标</font>**<font style="color:rgb(51, 51, 51);">：适应特定任务（分类、检测、分割等）。</font>
    - **<font style="color:rgb(51, 51, 51);">策略</font>**<font style="color:rgb(51, 51, 51);">：全模型微调或部分层微调，学习率更低。</font>
3. **混合训练（改进变体）**：
    - <font style="color:rgb(51, 51, 51);">结合 CNN（如 Hybrid ViT）或引入蒸馏（DeiT）。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 全局注意力机制，擅长捕捉长距离依赖</font> | <font style="color:rgb(51, 51, 51);">1. 数据效率低，依赖大规模预训练</font> |
| <font style="color:rgb(51, 51, 51);">2. 并行计算友好，适合硬件加速</font> | <font style="color:rgb(51, 51, 51);">2. 计算复杂度高（序列长度平方级）</font> |
| <font style="color:rgb(51, 51, 51);">3. 可扩展性强（模型深度/宽度易调整）</font> | <font style="color:rgb(51, 51, 51);">3. 缺乏局部归纳偏置，小数据集易过拟合</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">（ImageNet、CIFAR）。</font>
2. **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">（DETR、ViT-FRCNN）。</font>
3. **<font style="color:rgb(51, 51, 51);">图像分割</font>**<font style="color:rgb(51, 51, 51);">（SETR、Segmenter）。</font>
4. **<font style="color:rgb(51, 51, 51);">视频理解</font>**<font style="color:rgb(51, 51, 51);">（TimeSformer、ViViT）。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">数据效率优化</font>**
    - **<font style="color:rgb(51, 51, 51);">DeiT</font>**<font style="color:rgb(51, 51, 51);">：通过蒸馏从 CNN 中学习，减少数据依赖。</font>
2. **<font style="color:rgb(51, 51, 51);">计算效率优化</font>**
    - **<font style="color:rgb(51, 51, 51);">Swin Transformer</font>**<font style="color:rgb(51, 51, 51);">：引入局部窗口注意力，降低计算量。</font>
3. **<font style="color:rgb(51, 51, 51);">局部-全局结合</font>**
    - **<font style="color:rgb(51, 51, 51);">Hybrid ViT</font>**<font style="color:rgb(51, 51, 51);">：使用 CNN 提取底层特征，再输入 Transformer。</font>
4. **<font style="color:rgb(51, 51, 51);">多模态扩展</font>**
    - **<font style="color:rgb(51, 51, 51);">CLIP</font>**<font style="color:rgb(51, 51, 51);">：联合训练图像和文本编码器。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class PatchEmbedding(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.norm = nn.LayerNorm(embed_dim)
        self.pos_embed = nn.Parameter(torch.randn(1, (img_size//patch_size)**2 + 1, embed_dim))

    def forward(self, x):
        x = self.proj(x)  # [B, C, H, W] → [B, D, H/P, W/P]
        x = rearrange(x, "b c h w → b (h w) c")
        x = self.norm(x)
        # 添加 [CLS] token
        cls_token = nn.Parameter(torch.randn(1, 1, embed_dim)).expand(x.shape[0], -1, -1)
        x = torch.cat([cls_token, x], dim=1)
        x += self.pos_embed
        return x

class ViT(nn.Module):
    def __init__(self, num_layers=12, num_heads=12, mlp_dim=3072):
        super().__init__()
        self.patch_embed = PatchEmbedding()
        self.encoder_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=768, nhead=num_heads, dim_feedforward=mlp_dim)
            for _ in range(num_layers)
        ])
        self.head = nn.Linear(768, num_classes)

    def forward(self, x):
        x = self.patch_embed(x)
        for layer in self.encoder_layers:
            x = layer(x)
        cls_output = x[:, 0, :]
        return self.head(cls_output)

# 示例用法
model = ViT(num_classes=1000)
x = torch.randn(1, 3, 224, 224)
output = model(x)
print(output.shape)  # torch.Size([1, 1000])

```

```python
from torch.optim import AdamW
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import torchvision.transforms as T

# 数据加载
transform = T.Compose([
    T.Resize(224),
    T.ToTensor(),
])
dataset = CIFAR10(root="data", train=True, download=True, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 模型与优化器
model = ViT(num_classes=10)
optimizer = AdamW(model.parameters(), lr=1e-4)
criterion = nn.CrossEntropyLoss()

# 训练循环
for epoch in range(10):
    for images, labels in dataloader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

```

## DeiT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">DeiT（Data-efficient Image Transformer）</font>**<font style="color:rgb(51, 51, 51);"> 是 Facebook Research 在 2020 年提出的改进版视觉 Transformer，旨在解决 ViT（Vision Transformer）</font>**<font style="color:#ED740C;">依赖大规模预训练数据的问题</font>**<font style="color:rgb(51, 51, 51);">。ViT 需要 JFT-300M 等超大数据集才能达到与 CNN 相当的性能，</font>**<font style="color:#ED740C;">而 DeiT 通过知识蒸馏（Knowledge Distillation）和高效训练策略，仅用 ImageNet-1K（1.2M 图像）即可训练高性能 Transformer，推动 ViT 在资源有限场景下的应用。</font>**

+ **<font style="color:rgb(51, 51, 51);">论文</font>**<font style="color:rgb(51, 51, 51);">：</font>[《Training data-efficient image transformers & distillation through attention》](https://arxiv.org/abs/2012.12877)
+ **<font style="color:rgb(51, 51, 51);">官方代码</font>**<font style="color:rgb(51, 51, 51);">：</font>[https://github.com/facebookresearch/deit](https://github.com/facebookresearch/deit)

:::

<font style="color:rgb(51, 51, 51);">DeiT 通过蒸馏技术显著降低了 ViT 的数据需求，成为轻量级视觉 Transformer 的标杆，为实际工业部署提供了高效解决方案。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741086834536-c06b374e-218a-4d84-9d97-5d5dda8c1192.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **蒸馏 Token（Distillation Token）**
    - <font style="color:rgb(51, 51, 51);">在输入序列中引入</font>**<font style="color:#74B602;">可学习的蒸馏标记（与 [CLS] 标记并行）</font>**<font style="color:rgb(51, 51, 51);">，直接学习教师模型（如 CNN）的输出分布。</font>
    - <font style="color:rgb(51, 51, 51);">比传统蒸馏（仅用标签概率）更高效，尤其对小模型效果显著。</font>
2. **硬蒸馏与软蒸馏结合**
    - **<font style="color:rgb(51, 51, 51);">硬蒸馏</font>**<font style="color:rgb(51, 51, 51);">：将教师模型的预测类别（硬标签）作为监督信号。</font>
    - **<font style="color:rgb(51, 51, 51);">软蒸馏</font>**<font style="color:rgb(51, 51, 51);">：使用教师模型的输出概率（软标签）指导训练。</font>
3. **高效数据增强**
    - <font style="color:rgb(51, 51, 51);">结合 RandAugment、MixUp、CutMix 等策略，提升数据利用率。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据集</font>**<font style="color:rgb(51, 51, 51);">：ImageNet-1K（1.28M 训练图像，1k 类别）。</font>
+ **<font style="color:rgb(51, 51, 51);">教师模型</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">预训练的 CNN（如 RegNetY-16GF 或 ResNet-152）。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">RandAugment（随机增强强度自适应）、Erasing、重复增强（Repeated Augmentation）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

**<font style="color:rgb(51, 51, 51);">关键改进</font>**

1. **蒸馏 Token 处理**
    - <font style="color:rgb(51, 51, 51);">蒸馏 Token 与 [CLS] Token 并行输入 Transformer，通过自注意力交互。</font>
    - <font style="color:rgb(51, 51, 51);">最终输出两个预测结果：学生模型预测（[CLS]）和教师蒸馏预测（Distillation）。</font>
2. **损失函数设计**
    - <font style="color:rgb(51, 51, 51);">总损失 = 学生分类损失（CE） + 蒸馏损失（KL 散度）。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **教师模型准备**
    - <font style="color:rgb(51, 51, 51);">使用预训练 CNN 生成图像标签（硬标签）或概率分布（软标签）。</font>
2. **学生模型训练**
    - **<font style="color:rgb(51, 51, 51);">输入</font>**<font style="color:rgb(51, 51, 51);">：图像分块 + [CLS] Token + Distillation Token。</font>
    - **<font style="color:rgb(51, 51, 51);">目标 1</font>**<font style="color:rgb(51, 51, 51);">（学生损失）：[CLS] 预测与真实标签的交叉熵。</font>
    - **<font style="color:rgb(51, 51, 51);">目标 2</font>**<font style="color:rgb(51, 51, 51);">（蒸馏损失）：Distillation 预测与教师输出的 KL 散度。</font>
    - **<font style="color:rgb(51, 51, 51);">优化器</font>**<font style="color:rgb(51, 51, 51);">：AdamW，余弦学习率衰减，权重衰减分层设置。</font>
3. **训练技巧**
    - **<font style="color:rgb(51, 51, 51);">重复增强</font>**<font style="color:rgb(51, 51, 51);">：同一图像的不同增强版本在同一批次中出现，提升泛化性。</font>
    - **<font style="color:rgb(51, 51, 51);">随机深度（Stochastic Depth）</font>**<font style="color:rgb(51, 51, 51);">：随机丢弃部分层，防止过拟合。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

| **优点** | **缺点** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">1. 数据高效，仅需 ImageNet-1K 即可训练</font> | <font style="color:rgb(51, 51, 51);">1. 依赖教师模型的质量</font> |
| <font style="color:rgb(51, 51, 51);">2. 训练速度快（比 ViT 收敛更快）</font> | <font style="color:rgb(51, 51, 51);">2. 蒸馏 Token 增加模型参数量</font> |
| <font style="color:rgb(51, 51, 51);">3. 支持模型压缩（如 Tiny-DeiT）</font> | <font style="color:rgb(51, 51, 51);">3. 对数据增强策略敏感</font> |


:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：轻量级部署（移动端、边缘设备）。</font>
2. **<font style="color:rgb(51, 51, 51);">迁移学习</font>**<font style="color:rgb(51, 51, 51);">：作为下游任务（检测、分割）的预训练模型。</font>
3. **<font style="color:rgb(51, 51, 51);">联邦学习</font>**<font style="color:rgb(51, 51, 51);">：适应分布式小数据场景。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">无教师蒸馏：  </font>**<font style="color:rgb(51, 51, 51);">自蒸馏（Self-Distillation）：同一模型不同阶段的知识迁移。</font>
2. **<font style="color:rgb(51, 51, 51);">动态蒸馏：</font>**<font style="color:rgb(51, 51, 51);">教师模型在线更新（如 EMA 策略）。</font>
3. **<font style="color:rgb(51, 51, 51);">多教师融合：</font>**<font style="color:rgb(51, 51, 51);">结合多个教师模型的输出提升鲁棒性。</font>
4. **<font style="color:rgb(51, 51, 51);">结构优化：</font>**<font style="color:rgb(51, 51, 51);">DeiT-III：引入 LayerScale 和 Class-Attention 提升性能。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from timm.models.vision_transformer import Block, PatchEmbed

class DeiT(nn.Module):
    def __init__(self, img_size=224, patch_size=16, embed_dim=768, depth=12, num_heads=12):
        super().__init__()
        self.patch_embed = PatchEmbed(img_size, patch_size, 3, embed_dim)
        num_patches = self.patch_embed.num_patches
        # 初始化 [CLS] Token 和 Distillation Token
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.dist_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        # 位置编码
        self.pos_embed = nn.Parameter(torch.randn(1, num_patches + 2, embed_dim))
        # Transformer 编码器
        self.blocks = nn.ModuleList([Block(embed_dim, num_heads) for _ in range(depth)])
        # 分类头
        self.head = nn.Linear(embed_dim, 1000)
        self.head_dist = nn.Linear(embed_dim, 1000)

    def forward(self, x):
        B = x.shape[0]
        x = self.patch_embed(x)  # [B, N, D]
        # 添加 [CLS] 和 Distillation Token
        cls_tokens = self.cls_token.expand(B, -1, -1)
        dist_tokens = self.dist_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, dist_tokens, x), dim=1)
        x += self.pos_embed
        # 经过 Transformer 层
        for blk in self.blocks:
            x = blk(x)
        # 分离输出
        cls_out = x[:, 0]
        dist_out = x[:, 1]
        return self.head(cls_out), self.head_dist(dist_out)

# 示例用法
model = DeiT()
x = torch.randn(1, 3, 224, 224)
logits_cls, logits_dist = model(x)
print(logits_cls.shape)  # torch.Size([1, 1000])

```

```python
from torch.optim import AdamW
import torch.nn.functional as F

# 初始化
model = DeiT()
teacher_model = torch.hub.load('pytorch/vision', 'resnet152', pretrained=True)
optimizer = AdamW(model.parameters(), lr=1e-4)

# 蒸馏损失（软标签）
def distillation_loss(student_logits, teacher_logits, temperature=2.0):
    student_probs = F.log_softmax(student_logits / temperature, dim=1)
    teacher_probs = F.softmax(teacher_logits / temperature, dim=1)
    return F.kl_div(student_probs, teacher_probs, reduction="batchmean") * (temperature ** 2)

# 训练循环
for images, labels in dataloader:
    # 教师模型预测（不更新梯度）
    with torch.no_grad():
        teacher_logits = teacher_model(images)
    # 学生模型预测
    logits_cls, logits_dist = model(images)
    # 计算损失
    loss_cls = F.cross_entropy(logits_cls, labels)
    loss_dist = distillation_loss(logits_dist, teacher_logits)
    loss = 0.5 * loss_cls + 0.5 * loss_dist
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

```

## Swin Transformer
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Swin Transformer是微软亚洲研究院2021年提出的</font>**<font style="color:rgb(51, 51, 51);">层级化视觉Transformer</font>**<font style="color:rgb(51, 51, 51);">，针对传统ViT的</font>**<font style="color:rgb(51, 51, 51);">计算复杂度高</font>**<font style="color:rgb(51, 51, 51);">和</font>**<font style="color:rgb(51, 51, 51);">缺乏空间层次性</font>**<font style="color:rgb(51, 51, 51);">问题而设计。其背景特点包括：</font>

+ **<font style="color:rgb(51, 51, 51);">视觉任务需求</font>**<font style="color:rgb(51, 51, 51);">：CNN的层次化特征提取优势需要与Transformer全局建模能力结合</font>
+ **<font style="color:rgb(51, 51, 51);">效率瓶颈</font>**<font style="color:rgb(51, 51, 51);">：ViT的全局注意力计算复杂度为O(n²)，难以处理高分辨率图像（如目标检测/分割）</font>
+ **<font style="color:rgb(51, 51, 51);">核心思想</font>**<font style="color:rgb(51, 51, 51);">：通过**滑动窗口（Shifted Window）**实现局部注意力，构建类似CNN的层次化特征金字塔</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087210932-ca6753c8-5cf8-497c-8ce1-4425fd9eb7a7.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

| **维度** | **创新描述** |
| --- | --- |
| **<font style="color:rgb(51, 51, 51);">窗口划分</font>** | <font style="color:rgb(51, 51, 51);">将特征图划分为不重叠窗口，计算</font>**<font style="color:#74B602;">窗口内自注意力</font>**<font style="color:rgb(51, 51, 51);">（计算复杂度从O(n²)降为O(n)）</font> |
| **<font style="color:rgb(51, 51, 51);">移位窗口</font>** | <font style="color:rgb(51, 51, 51);">通过窗口滑动实现</font>**<font style="color:#74B602;">跨窗口信息交互，避免全局计算</font>** |
| **<font style="color:rgb(51, 51, 51);">层级结构</font>** | <font style="color:rgb(51, 51, 51);">4-stage下采样结构（类似ResNet），输出</font>**<font style="color:#74B602;">多尺度特征图</font>** |
| **<font style="color:rgb(51, 51, 51);">相对位置编码</font>** | <font style="color:rgb(51, 51, 51);">在计算注意力时加入</font>**<font style="color:#74B602;">相对位置偏置</font>**<font style="color:rgb(51, 51, 51);">，提升空间感知能力</font> |


:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

| **阶段** | **数据类型** | **规模** | **预处理** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">预训练</font>** | <font style="color:rgb(51, 51, 51);">ImageNet-1K/22K</font> | <font style="color:rgb(51, 51, 51);">1.28M/14M</font> | <font style="color:rgb(51, 51, 51);">RandAugment, Mixup, CutMix</font> |
| **<font style="color:rgb(51, 51, 51);">检测微调</font>** | <font style="color:rgb(51, 51, 51);">COCO 2017</font> | <font style="color:rgb(51, 51, 51);">118K</font> | <font style="color:rgb(51, 51, 51);">多尺度训练 (480~800px)</font> |
| **<font style="color:rgb(51, 51, 51);">分割微调</font>** | <font style="color:rgb(51, 51, 51);">ADE20K</font> | <font style="color:rgb(51, 51, 51);">25K</font> | <font style="color:rgb(51, 51, 51);">随机裁剪至512x512</font> |


:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">层级化架构（以Swin-T为例）</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087175978-29788f6d-7d18-4f16-89c2-35da554b0fa5.png)

```python
class SwinTransformer(nn.Module):
    def __init__(self):
        # Stage 1: Patch分割 + 线性嵌入
        self.patch_embed = PatchEmbed(img_size=224, patch_size=4, in_chans=3, embed_dim=96)

        # 4个阶段（逐渐下采样）
        self.stages = nn.ModuleList([
            SwinStage(dim=96,  depth=2, num_heads=3, window_size=7),
            SwinStage(dim=192, depth=2, num_heads=6, window_size=7),  # 下采样2x
            SwinStage(dim=384, depth=6, num_heads=12, window_size=7), # 下采样4x
            SwinStage(dim=768, depth=2, num_heads=24, window_size=7)  # 下采样8x
        ])

        # 分类头
        self.head = nn.Linear(768, num_classes)
```

2. **<font style="color:rgb(51, 51, 51);">Swin Transformer Block结构</font>**

Swin Transformer Block有两种block形式，一个是W-MSA，另一个是SW-MSA。注意这两个结构是成对使用的，先使用W-MSA再使用SW-MSA。因此Swin Transformer Block都是偶数。

+ <font style="color:rgba(0, 0, 0, 0.75);background-color:#D9EAFC;">Windows Multi-head Self-Attention（W-MSA）</font>

W-MSA将特征图划分为多个大小为M × M的小窗口（windows），每个小窗口里有M<sup>2</sup>个patch，并在每个窗口内独立地进行MSA。（一个大小为H × W的特征图，下面这个小例子中窗口大小是M = 2，因此特征图被划分成个小窗口），计算量将显著减少。

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741091364826-1396ca51-2a5b-4b7b-92e2-98b729ef57ba.png)

+ <font style="color:rgba(0, 0, 0, 0.75);background-color:#D9EAFC;">Shifted Windows Multi-Head Self-Attention（SW-MSA）</font>

<font style="color:rgb(77, 77, 77);">然而W-MSA也存在一些问题，W-MSA只会在每个窗口内进行自注意力计算，窗口之间无法进行信息传递，为了解决该问题，作者提出了SW-MSA模块，即对窗口进行偏移，如下图所示：</font>



![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741087187355-fa8584f7-88ce-4b3e-940f-64a42e708d97.png)

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **预训练**（ImageNet）：
    - <font style="color:rgb(51, 51, 51);">优化器：AdamW（lr=0.001, weight_decay=0.05）</font>
    - <font style="color:rgb(51, 51, 51);">训练策略：300 epochs，cosine学习率衰减</font>
    - <font style="color:rgb(51, 51, 51);">数据增强：RandErasing, ColorJitter</font>
2. **下游任务微调**：
    - <font style="color:rgb(51, 51, 51);">目标检测（Mask R-CNN）：多尺度训练，AP^box从42.7提升到50.4</font>
    - <font style="color:rgb(51, 51, 51);">语义分割（UPerNet）：mIoU达到53.5（ADE20K）</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">线性计算复杂度（相比ViT的平方复杂度）</font>
+ <font style="color:rgb(51, 51, 51);">多尺度输出适配密集预测任务（检测/分割）</font>
+ <font style="color:rgb(51, 51, 51);">在COCO上超越ResNet-50约4.5 AP</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">窗口移位操作增加实现复杂度</font>
+ <font style="color:rgb(51, 51, 51);">小规模数据（如CIFAR）上表现不如CNN</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

| **场景** | **典型应用** |
| --- | --- |
| <font style="color:rgb(51, 51, 51);">图像分类</font> | <font style="color:rgb(51, 51, 51);">ImageNet Top-1 Acc 87.3% (Swin-L)</font> |
| <font style="color:rgb(51, 51, 51);">目标检测</font> | <font style="color:rgb(51, 51, 51);">COCO检测任务（Swin + Mask R-CNN）</font> |
| <font style="color:rgb(51, 51, 51);">语义分割</font> | <font style="color:rgb(51, 51, 51);">ADE20K语义分割（Swin + UPerNet）</font> |
| <font style="color:rgb(51, 51, 51);">视频分析</font> | <font style="color:rgb(51, 51, 51);">时空扩展版本Video Swin Transformer</font> |


:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

1. **效率优化**：
    - <font style="color:rgb(51, 51, 51);">CSWin Transformer：引入十字形窗口注意力</font>
    - <font style="color:rgb(51, 51, 51);">SwinIR：结合图像复原任务优化窗口划分</font>
2. **性能提升**：
    - <font style="color:rgb(51, 51, 51);">SwinV2：使用对数间隔连续位置偏置（解决大模型训练不稳定）</font>
    - <font style="color:rgb(51, 51, 51);">混合架构：Swin-Unet用于医学图像分割</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
from torch import nn

class WindowAttention(nn.Module):
    """基于移位窗口的多头自注意力"""
    def __init__(self, dim, window_size, num_heads):
        super().__init__()
        self.dim = dim
        self.window_size = window_size
        self.num_heads = num_heads
        
        # 相对位置编码表
        self.relative_position_bias_table = nn.Parameter(
            torch.zeros((2*window_size-1)**2, num_heads))
        
        # 生成相对位置索引
        coords = torch.stack(torch.meshgrid(
            [torch.arange(window_size), torch.arange(window_size)]))
        coords_flatten = torch.flatten(coords, 1)
        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]
        relative_coords = relative_coords.permute(1, 2, 0).contiguous()
        relative_coords[:, :, 0] += window_size - 1
        self.register_buffer("relative_position_index", relative_coords.sum(-1))
    
    def forward(self, x):
        B, H, W, C = x.shape
        x = x.view(B, H//self.window_size, self.window_size,
                   W//self.window_size, self.window_size, C)
        x = x.permute(0, 1, 3, 2, 4, 5).contiguous().view(-1, self.window_size*self.window_size, C)
        
        # 计算注意力（含相对位置偏置）
        qkv = self.qkv(x).reshape(-1, self.window_size*self.window_size, 3, self.num_heads, C//self.num_heads)
        attn = (q @ q.transpose(-2, -1)) * self.scale
        relative_bias = self.relative_position_bias_table[self.relative_position_index.view(-1)]
        attn += relative_bias.view(1, self.num_heads, self.ws*self.ws, self.ws*self.ws)
        attn = self.softmax(attn)
        
        x = (attn @ v).transpose(1, 2).reshape(-1, self.ws*self.ws, C)
        return x.view(B, H, W, C)

class SwinBlock(nn.Module):
    """包含常规窗口和移位窗口的双分支结构"""
    def __init__(self, dim, num_heads, window_size):
        super().__init__()
        # 常规窗口分支
        self.norm1 = nn.LayerNorm(dim)
        self.attn1 = WindowAttention(dim, window_size, num_heads)
        
        # 移位窗口分支（移位量为window_size//2）
        self.norm2 = nn.LayerNorm(dim)
        self.attn2 = WindowAttention(dim, window_size, num_heads, shift_size=window_size//2)
        
        self.mlp = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, dim*4),
            nn.GELU(),
            nn.Linear(dim*4, dim)
        )
    
    def forward(self, x):
        # 第一分支
        x = x + self.attn1(self.norm1(x))
        # 第二分支（移位窗口）
        x = x + self.attn2(self.norm2(x))
        x = x + self.mlp(x)
        return x

```





## NaViT
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">一般标准的预训练好的ViT，通常是将图片处理成正方形（长:宽=1:1）。这样处理后通常图片会失真，导致模型理解上有信息损失或引入一些误导。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">原生动态分辨率方法具体是怎么实现的呢？ 核心方法是采用了</font>**<font style="color:#ED740C;">NaViT的</font>**[**<font style="color:#ED740C;">Patch n’ Pack</font>**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**<font style="color:#ED740C;">技术，把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率</font>**<font style="color:rgb(25, 27, 31);">。同时在</font>**<font style="color:#ED740C;">一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐</font>**<font style="color:rgb(25, 27, 31);">，在性能上始终优于传统的ViT。</font>

**<font style="color:rgb(25, 27, 31);">paper</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://arxiv.org/pdf/2307.06304](https://arxiv.org/pdf/2307.06304)

**参考：**[**多模态技术梳理：Qwen-VL系列**](https://zhuanlan.zhihu.com/p/25267823390)**  **[**24年下半年较新的VLM架构**](https://zhuanlan.zhihu.com/p/11503653276)

:::

:::color5
**<font style="color:#601BDE;">1.传统ViT 对比 NaViT</font>**

:::

+ **传统的ViT**：将任何图片数据都处理成定长的Patch序列，然后输入给Vision Encoder，这种统一定长的输入是对硬件计算非常友好的，非常好组Batch，并且不需要任何padding处理。Batch序列中每个位置的计算都是有效的。
+ **NaViT的**[**Patch n’ Pack**](https://zhida.zhihu.com/search?content_id=254075742&content_type=Article&match_order=1&q=Patch+n%E2%80%99+Pack&zhida_source=entity)**技术：把不同图像的多个patch打包到一个序列，能保留不同图片的可变分辨率。同时在一个次序列计算中同时可处理多个图像，提升了模型计算的吞吐，在性能上始终优于传统的ViT**。其性能提升主要来源于Pack处理后，一个序列包括多个图片能同时计算，使得在固定计算预算下，动态分辨率方法能训练更多样本，从而带来更好的性能。

:::color5
**<font style="color:#601BDE;">2.处理过程示例</font>**

:::

**<font style="color:rgb(83, 88, 97);">举</font>****例**：假设我们5张图片： I<sub>1</sub>∼I<sub>5</sub> ，且patch长度为： 2∼6 ，即图片Patch后长度为： {I<sub>1</sub>:2, I<sub>2</sub>:3, I<sub>3</sub>:4, I<sub>4</sub>:5 , I<sub>5</sub>:6} 。为了描述简单，我们假设模型设置Batch_Size=2，并且正好处理这5张图片到一个Batch中。

1. **<font style="color:rgb(25, 27, 31);">将5张图片进行Pack，放到2个序列中</font>**

<font style="color:rgb(25, 27, 31);">一个很简单的方式是将3个Patch较短的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> ，2个较长Patch的图片放到一个序列 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);"> 。符号化为： </font><font style="color:rgb(25, 27, 31);">Batch={S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">,S</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">}</font><font style="color:rgb(25, 27, 31);"> ，其中 </font><font style="color:rgb(25, 27, 31);">S1={I</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);">:2,I</font><sub><font style="color:rgb(25, 27, 31);">2</font></sub><font style="color:rgb(25, 27, 31);">:3,I</font><sub><font style="color:rgb(25, 27, 31);">3</font></sub><font style="color:rgb(25, 27, 31);">:4}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">9</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">S2={I</font><sub><font style="color:rgb(25, 27, 31);">4</font></sub><font style="color:rgb(25, 27, 31);">:5,I</font><sub><font style="color:rgb(25, 27, 31);">5</font></sub><font style="color:rgb(25, 27, 31);">:6}</font><font style="color:rgb(25, 27, 31);"> 序列长度为 </font><font style="color:rgb(25, 27, 31);">11</font>

2. **<font style="color:rgb(25, 27, 31);">Batch内做序列Padding对齐处理</font>**

<font style="color:rgb(25, 27, 31);">根据Batch内最长序列，通过F.pad方法做序列对齐，在序列前后增加Padding token，该例子中由于 </font><font style="color:rgb(25, 27, 31);">S</font><sub><font style="color:rgb(25, 27, 31);">1</font></sub><font style="color:rgb(25, 27, 31);"> 较短，需要在末尾增加Padding token，处理后，如下图所示</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742269727057-53d999b7-845e-4997-a739-f0ae5cf978d3.png)

3. **<font style="color:rgb(25, 27, 31);">通过设置Attention Mask保证同Sequence中各图片计算隔离</font>**

<font style="color:rgb(25, 27, 31);">一个序列中有多张图片输入，在计算时要必须保证各图片的Attention计算是相互隔离的。实现上通过对Attention Mask矩阵做特殊的设置，来保证计算隔离。计算Attention Mask的过程如下：</font>

<font style="color:rgb(25, 27, 31);">首先，记录序列中每个图片起止token位置（包括初始0位置），得到两个位置序列为：</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);">={0,2,5,9}</font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);">={0,5,11}</font><font style="color:rgb(25, 27, 31);"> ， </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);"> 中连续的两个数 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> 表示一张图片在序列中的长度为 </font><font style="color:rgb(25, 27, 31);">k−j</font><font style="color:rgb(25, 27, 31);"> 个特征，且特征的起止位置为： </font><font style="color:rgb(25, 27, 31);">j</font><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">k−1</font><font style="color:rgb(25, 27, 31);"> 。</font>

<font style="color:rgb(25, 27, 31);">然后，分别用 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s1</font></sub><font style="color:rgb(25, 27, 31);"> 和 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">s2</font></sub><font style="color:rgb(25, 27, 31);"> 来计算二维Attention mask矩阵，计算方式为：先初始化一个全0的mask矩阵，然后遍历每个 </font><font style="color:rgb(25, 27, 31);">P</font><sub><font style="color:rgb(25, 27, 31);">st</font></sub><font style="color:rgb(25, 27, 31);">，取 </font><font style="color:rgb(25, 27, 31);">[i,i+1]</font><font style="color:rgb(25, 27, 31);"> 位置的两个数字 </font><font style="color:rgb(25, 27, 31);">(j,k)</font><font style="color:rgb(25, 27, 31);"> ，使得矩阵行列坐标都满足在 </font><font style="color:rgb(25, 27, 31);">[j,k−1]</font><font style="color:rgb(25, 27, 31);"> 区间范围的位置置1。两个序列计算后的Mask矩阵，如下图所示。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742278208815-33fb8129-af9d-4c4a-bbb3-a0b220e4212a.png)

<font style="color:rgb(25, 27, 31);">  
</font><font style="color:rgb(25, 27, 31);">计算好了上面的Attention Mask矩阵，在过Vision Encoder网络时，</font>**<font style="color:#74B602;">将Attention Mask作用在Attention计算上，就会隔离同一序列中不同图像的Attention计算</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:rgb(25, 27, 31);">InternViT</font>
:::color3
**简介：**<font style="color:rgb(25, 27, 31);">InternViT仍然延用ViT的结构主要由</font>**<font style="color:#74B602;">VisionEmbeddings和VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">两个大模块组成</font>

**paper：**[**https://arxiv.org/pdf/2010.11929**](https://arxiv.org/pdf/2010.11929)

**参考：**[**https://zhuanlan.zhihu.com/p/702481058**](https://zhuanlan.zhihu.com/p/702481058)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1742528314276-7f3161f2-a40c-4bb2-ab9e-7f2e51ff721a.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

<font style="color:rgb(25, 27, 31);">InternViT仍然延用ViT的结构主要由</font>**<font style="color:#74B602;">VisionEmbeddings和VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">两个大模块组成，</font>

+ **<font style="color:rgb(25, 27, 31);">VisionEmbeddings：</font>**<font style="color:rgb(25, 27, 31);">负责将图像编码成Embedding，并且position embedding采用了可学习的方式，forward时，会将图像patch embedding和position embedding相加，得到ViT的输入，然后送入VisionEncoder进行推理。</font>
+ **<font style="color:rgb(25, 27, 31);">VisionEncoder</font>**<font style="color:rgb(25, 27, 31);">：中包含多层标准的Transformer层，也就是InternVisionEncoderLayer。</font>

:::color5
**<font style="color:#601BDE;">2.config</font>**

:::

```python
num_channels=3,
patch_size=14,
image_size=224,
qkv_bias=False,
hidden_size=3200,
num_attention_heads=25,
intermediate_size=12800,
qk_normalization=True,
num_hidden_layers=48,
use_flash_attn=True,
hidden_act='gelu',
norm_type='rms_norm',
layer_norm_eps=1e-6,
dropout=0.0,
drop_path_rate=0.0,
attention_dropout=0.0,
initializer_range=0.02,
initializer_factor=0.1,
```

:::color5
**<font style="color:#601BDE;">3.代码实现</font>**

:::

```python
class InternVisionModel(PreTrainedModel):
    main_input_name = 'pixel_values'
    _supports_flash_attn_2 = True
    config_class = InternVisionConfig
    _no_split_modules = ['InternVisionEncoderLayer']

    def __init__(self, config: InternVisionConfig):
        super().__init__(config)
        self.config = config

        self.embeddings = InternVisionEmbeddings(config)
        self.encoder = InternVisionEncoder(config)

    def resize_pos_embeddings(self, old_size, new_size, patch_size):
        pos_emb = self.embeddings.position_embedding
        _, num_positions, embed_dim = pos_emb.shape
        cls_emb = pos_emb[:, :1, :]
        pos_emb = pos_emb[:, 1:, :].reshape(1, old_size // patch_size, old_size // patch_size, -1).permute(0, 3, 1, 2)
        pos_emb = F.interpolate(pos_emb.float(), size=new_size // patch_size, mode='bicubic', align_corners=False)
        pos_emb = pos_emb.to(cls_emb.dtype).reshape(1, embed_dim, -1).permute(0, 2, 1)
        pos_emb = torch.cat([cls_emb, pos_emb], dim=1)
        self.embeddings.position_embedding = nn.Parameter(pos_emb)
        self.embeddings.image_size = new_size
        logger.info('Resized position embeddings from {} to {}'.format(old_size, new_size))

    def get_input_embeddings(self):
        return self.embeddings

    def forward(
            self,
            pixel_values: Optional[torch.FloatTensor] = None,
            output_hidden_states: Optional[bool] = None,
            return_dict: Optional[bool] = None,
            pixel_embeds: Optional[torch.FloatTensor] = None,
    ) -> Union[Tuple, BaseModelOutputWithPooling]:
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if pixel_values is None and pixel_embeds is None:
            raise ValueError('You have to specify pixel_values or pixel_embeds')

        if pixel_embeds is not None:
            hidden_states = pixel_embeds
        else:
            if len(pixel_values.shape) == 4:
                # print("intern vit forward pixel_values dtype:\n", pixel_values.dtype)
                pixel_values=pixel_values.to(torch.bfloat16)
                # print("convert intern vit forward pixel_values dtype:\n", pixel_values.dtype)
                hidden_states = self.embeddings(pixel_values)
            else:
                raise ValueError(f'wrong pixel_values size: {pixel_values.shape}')
        encoder_outputs = self.encoder(
            inputs_embeds=hidden_states,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        last_hidden_state = encoder_outputs.last_hidden_state
        pooled_output = last_hidden_state[:, 0, :]

        if not return_dict:
            return (last_hidden_state, pooled_output) + encoder_outputs[1:]

        return BaseModelOutputWithPooling(
            last_hidden_state=last_hidden_state,
            pooler_output=pooled_output,
            hidden_states=encoder_outputs.hidden_states,
            attentions=encoder_outputs.attentions,
        )

```

##  EVA02
[https://blog.csdn.net/sinat_37574187/article/details/142938184](https://blog.csdn.net/sinat_37574187/article/details/142938184)





##  [LLM2CLIP](https://github.com/microsoft/LLM2CLIP)
[https://github.com/microsoft/LLM2CLIP](https://github.com/microsoft/LLM2CLIP)

<font style="color:rgb(51, 51, 51);">Pre-Training</font>







## MAE
<font style="color:rgb(51, 51, 51);">MAE (Masked Autoencoders Are Scalable Vision Learners) 模型详解</font>

:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">自监督学习需求</font>**<font style="color:rgb(51, 51, 51);">：传统监督学习依赖大量标注数据，成本高昂。自监督学习通过无标注数据预训练模型，提升泛化能力。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">图像掩码重建的启发</font>**<font style="color:rgb(51, 51, 51);">：NLP中BERT通过掩码语言建模（MLM）取得成功，启发视觉领域类似方法（如BEiT）。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">MAE定位</font>**<font style="color:rgb(51, 51, 51);">：何恺明团队提出的掩码自编码器，通过高比例随机掩码图像块并重建，学习高效视觉表示。</font>

:::

<font style="color:rgb(51, 51, 51);">MAE通过高比例掩码和像素级重建任务，推动了视觉自监督学习的发展。其高效的非对称架构设计为大规模预训练提供了新思路，后续工作可通过结合语义约束和多模态对齐进一步提升性能。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741092698055-73b1eb72-d118-4ca2-b86b-ca188351fcbc.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">非对称编码器-解码器架构</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">轻量编码器</font>**<font style="color:rgb(51, 51, 51);">：仅处理可见图像块（如25%可见），降低计算量。</font>
    - **<font style="color:rgb(51, 51, 51);">独立解码器</font>**<font style="color:rgb(51, 51, 51);">：接收编码特征和掩码标记，重建完整图像。</font>
+ **<font style="color:rgb(51, 51, 51);">高比例随机掩码</font>**<font style="color:rgb(51, 51, 51);">：掩码率高达75%，强制模型学习全局上下文推理。</font>
+ **<font style="color:rgb(51, 51, 51);">像素级重建目标</font>**<font style="color:rgb(51, 51, 51);">：直接预测掩码块的原始像素值，无需离散化或tokenizer。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">无标注图像数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">公开数据集：ImageNet-1K/21K（无需标签）。</font>
    - <font style="color:rgb(51, 51, 51);">大规模网络图片：如JFT-300M（论文中使用）。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像归一化为224x224分辨率。</font>
    - <font style="color:rgb(51, 51, 51);">随机裁剪、色彩抖动、水平翻转等增强。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741092591257-fda4ef64-936c-4bea-9f44-e6f42de7fca9.png)

+ **<font style="color:rgb(51, 51, 51);">编码器（ViT Backbone）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：未被掩码的图像块（如14x14块，每块16x16像素）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：标准Vision Transformer（ViT-Base/Large/Huge）。</font>
    - <font style="color:rgb(51, 51, 51);">输出：可见块的编码特征。</font>
+ **<font style="color:rgb(51, 51, 51);">解码器</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：编码特征 + 可学习的掩码标记（mask tokens）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：轻量级Transformer（更少层数，如4层）。</font>
    - <font style="color:rgb(51, 51, 51);">输出：重建的像素值（每个掩码块预测16x16x3像素）。</font>
+ **<font style="color:rgb(51, 51, 51);">掩码策略</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">随机选择75%的图像块进行掩码，剩余25%作为输入。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **图像分块与掩码**：
    - <font style="color:rgb(51, 51, 51);">将图像分割为不重叠的16x16块。</font>
    - <font style="color:rgb(51, 51, 51);">随机掩码75%的块，仅保留25%输入编码器。</font>
2. **编码器前向**：
    - <font style="color:rgb(51, 51, 51);">对可见块进行线性投影，加入位置编码。</font>
    - <font style="color:rgb(51, 51, 51);">通过ViT提取特征。</font>
3. **解码器重建**：
    - <font style="color:rgb(51, 51, 51);">将编码特征与掩码标记拼接，加入位置编码。</font>
    - <font style="color:rgb(51, 51, 51);">解码器输出每个掩码块的像素值。</font>
4. **损失计算**：
    - <font style="color:rgb(51, 51, 51);">均方误差（MSE）损失：比较重建像素与原始像素。</font>
    - <font style="color:rgb(51, 51, 51);">仅对掩码块计算损失。</font>
5. **微调**：
    - <font style="color:rgb(51, 51, 51);">预训练后，移除解码器，在编码器后添加任务头（分类、检测等）。</font>
    - <font style="color:rgb(51, 51, 51);">使用少量标注数据微调。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">训练高效：编码器仅处理部分图像块，计算量减少约75%。</font>
+ <font style="color:rgb(51, 51, 51);">泛化能力强：高掩码率迫使模型学习全局语义。</font>
+ <font style="color:rgb(51, 51, 51);">兼容下游任务：预训练模型可迁移至分类、检测、分割等任务。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">像素级重建对高频细节敏感，可能导致过拟合噪声。</font>
+ <font style="color:rgb(51, 51, 51);">重建任务与高层语义任务的优化目标不完全一致。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像分类</font>**<font style="color:rgb(51, 51, 51);">：微调编码器作为特征提取器。</font>
+ **<font style="color:rgb(51, 51, 51);">目标检测</font>**<font style="color:rgb(51, 51, 51);">：预训练模型作为检测主干网络（如Mask R-CNN）。</font>
+ **<font style="color:rgb(51, 51, 51);">语义分割</font>**<font style="color:rgb(51, 51, 51);">：输出密集特征图用于像素级预测。</font>
+ **<font style="color:rgb(51, 51, 51);">数据增强</font>**<font style="color:rgb(51, 51, 51);">：利用重建能力生成图像变体。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">多任务学习</font>**<font style="color:rgb(51, 51, 51);">：结合对比损失（如SimCLR）提升特征判别性。</font>
+ **<font style="color:rgb(51, 51, 51);">多尺度掩码</font>**<font style="color:rgb(51, 51, 51);">：混合不同块大小掩码（如16x16与32x32）。</font>
+ **<font style="color:rgb(51, 51, 51);">语义感知重建</font>**<font style="color:rgb(51, 51, 51);">：引入CLIP等模型约束高层语义一致性。</font>
+ **<font style="color:rgb(51, 51, 51);">动态掩码率</font>**<font style="color:rgb(51, 51, 51);">：根据图像内容自适应调整掩码比例。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
from einops import rearrange

class MAE(nn.Module):
    def __init__(self, encoder, decoder, mask_ratio=0.75):
        super().__init__()
        self.encoder = encoder  # ViT编码器
        self.decoder = decoder  # 轻量Transformer解码器
        self.mask_ratio = mask_ratio
        self.patch_size = 16
        self.embed_dim = encoder.embed_dim

        # 可学习的掩码标记
        self.mask_token = nn.Parameter(torch.randn(1, 1, self.embed_dim))

    def random_masking(self, x):
        N, L, D = x.shape  # L = (224/16)^2 = 196
        len_keep = int(L * (1 - self.mask_ratio))
        
        # 随机选择保留的索引
        ids_keep = torch.multinomial(torch.ones(L), len_keep, replacement=False)
        ids_mask = torch.ones(L, dtype=torch.bool)
        ids_mask[ids_keep] = False
        
        # 分离可见块与掩码块
        x_visible = x[:, ~ids_mask, :]
        return x_visible, ids_mask

    def forward(self, imgs):
        # 图像分块并嵌入
        patches = rearrange(imgs, 'b c (h p1) (w p2) -> b (h w) (p1 p2 c)', 
                            p1=self.patch_size, p2=self.patch_size)
        x = self.encoder.patch_embed(patches)  # [B, L, D]
        
        # 随机掩码
        x_visible, mask = self.random_masking(x)
        
        # 编码器处理可见块
        x_encoded = self.encoder(x_visible, mask=None)  # [B, len_keep, D]
        
        # 解码器输入：编码特征 + 掩码标记
        B, L = x.shape[:2]
        mask_tokens = self.mask_token.repeat(B, L - x_visible.shape[1], 1)
        x_full = torch.cat([x_encoded, mask_tokens], dim=1)
        x_decoded = self.decoder(x_full)  # [B, L, D]
        
        # 重建像素
        pred_pixels = self.decoder.to_pixels(x_decoded)  # [B, L, 16*16*3]
        return pred_pixels, mask

# 示例调用
class ViTEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.patch_embed = nn.Linear(16*16*3, 768)
        self.blocks = nn.TransformerEncoderLayer(d_model=768, nhead=12)
    
    def forward(self, x, mask):
        return self.blocks(x)

class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.TransformerDecoderLayer(d_model=768, nhead=12)
        self.to_pixels = nn.Linear(768, 16*16*3)
    
    def forward(self, x):
        return self.to_pixels(self.layers(x))

encoder = ViTEncoder()
decoder = Decoder()
model = MAE(encoder, decoder, mask_ratio=0.75)

# 训练循环
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
for imgs in dataloader:
    pred_pixels, mask = model(imgs)
    loss = ((pred_pixels - imgs)**2).mean(dim=-1)[mask].mean()
    loss.backward()
    optimizer.step()

```



# <font style="color:rgb(1, 1, 1);">多模态-Reasoning</font>
## Visual-RFT
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**视觉强化微调 Visual-RFT (visual reforce finetuning)**

+ <font style="color:rgb(25, 27, 31);">提出 </font>**<font style="color:rgb(25, 27, 31);">Visual-RFT</font>**<font style="color:rgb(25, 27, 31);">：首次将</font>**<font style="color:#ED740C;">基于 </font>**[**<font style="color:#ED740C;">GRPO</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)**<font style="color:#ED740C;"> 的强化学习策略应用于增强 LVLMs 的视觉感知和定位能力</font>**<font style="color:rgb(25, 27, 31);">，解决了数据稀缺场景下的微调问题。</font>
+ <font style="color:rgb(25, 27, 31);">设计</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">函数：</font>**<font style="color:#ED740C;">为不同视觉任务（如检测、分类）设计了高效的奖励函数</font>**<font style="color:rgb(25, 27, 31);">，简化了奖励计算。</font>
+ <font style="color:rgb(25, 27, 31);">广泛的实验验证：基于</font><font style="color:rgb(25, 27, 31);"> </font>[**<font style="color:rgb(9, 64, 142);">Qwen2-VL-2/7B</font>**](https://zhida.zhihu.com/search?content_id=254647528&content_type=Article&match_order=1&q=Qwen2-VL-2%2F7B&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">，</font>**<font style="color:rgb(25, 27, 31);">在多种视觉任务上验证了 Visual-RFT 的有效性，显著优于 SFT。</font>
+ **<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">代码和数据：提供了完整的训练代码、数据集和评估脚本，便于后续研究。</font>

:::

<font style="color:rgb(25, 27, 31);">Visual-RFT首先利用大型视觉语言模型（Large Vision-Language Models, LVLMs）为每个输入生成多个包含推理标记和最终答案的响应，然后通过我们提出的视觉感知可验证奖励函数，结合 </font>**<font style="color:rgb(25, 27, 31);">群体相对策略优化（Group Relative Policy Optimization, GRPO）</font>**<font style="color:rgb(25, 27, 31);">等策略优化算法来更新模型。</font>

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. <font style="color:rgb(25, 27, 31);">我们引入了 </font>**<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual Reinforcement Fine-Tuning, Visual-RFT）</font>**<font style="color:rgb(25, 27, 31);">，它将带有可验证奖励的强化学习扩展到视觉感知任务，这些任务在</font>**<font style="color:#74B602;">微调数据有限的情况下依然有效</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">我们</font>**<font style="color:#74B602;">为不同的视觉任务设计了不同的可验证奖励</font>**<font style="color:rgb(25, 27, 31);">，使得奖励计算高效且成本极低。这使得 DeepSeek R1 风格的强化学习能够无缝迁移到 LVLMs。</font>
3. <font style="color:rgb(25, 27, 31);">我们在多种视觉感知任务上进行了广泛的实验，包括</font>**<font style="color:#74B602;">细粒度图像分类、少样本目标检测、推理定位和开放词汇目标检测</font>**<font style="color:rgb(25, 27, 31);">。在所有设置中，Visual-RFT 均取得了显著的性能提升，大幅超越了监督微调基线。</font>
4. <font style="color:rgb(25, 27, 31);">我们在 GitHub 上完全</font>**<font style="color:rgb(25, 27, 31);">开源</font>**<font style="color:rgb(25, 27, 31);">了训练代码、训练数据和评估脚本，以促进进一步的研究。</font>

:::color5
**<font style="color:#601BDE;">2.RFT(强化微调)和SFT的主要区别在于数据</font>**

:::

**<font style="color:rgb(25, 27, 31);">强化微调（RFT）与以往的监督微调（Supervised Fine-Tuning, SFT）的主要区别在于数据效率</font>**<font style="color:rgb(25, 27, 31);">。以往的 SFT 范式直接模仿高质量、精心策划的数据中提供的“真实”答案，因此依赖于大量的训练数据。</font>

<font style="color:rgb(25, 27, 31);">相比之下，RFT 通过评估模型的响应并根据其</font>**<font style="color:#ED740C;">是否正确进行调整，帮助模型通过试错学习</font>**<font style="color:rgb(25, 27, 31);">。因此，</font>**<font style="color:#ED740C;">RFT 特别适用于数据稀缺的领域</font>**<font style="color:rgb(25, 27, 31);">。然而，以往的共识是，RFT 仅应用于科学（例如数学）和代码生成等任务。这是因为数学和编程具有清晰且客观的最终答案或测试用例，使得它们的奖励相对容易验证。在本文中，我们证明了 </font>**<font style="color:#ED740C;">RFT 可以应用于视觉感知任务，而不仅仅是数学和代码领域</font>**<font style="color:rgb(25, 27, 31);">。</font>

:::color5
**<font style="color:#601BDE;">3.视觉强化微调</font>**

:::

<font style="color:rgb(25, 27, 31);">视觉强化微调（Visual-RFT）框架。给定问题和视觉图像输入，策略模型生成多个包含推理步骤的响应。随后，使用</font>**<font style="color:rgb(25, 27, 31);">可验证奖励</font>**<font style="color:rgb(25, 27, 31);">（如交并比奖励和分类奖励）结合</font>**<font style="color:rgb(25, 27, 31);">策略梯度优化算法</font>**<font style="color:rgb(25, 27, 31);">来更新策略模型。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741334693920-bda1b180-762d-494a-ad86-dbd607f8b6a3.png)

**训练步骤**

1. <font style="color:rgb(25, 27, 31);">用户提供的多模态输入数据包括图像和问题。</font>

```python
imag 1
Q:图中卡车那部分是可以打开的？
..
imag n
Q：这朵花是什么品种？
```

2. <font style="color:rgb(25, 27, 31);">策略模型 </font><font style="color:rgb(25, 27, 31);">πθ</font><font style="color:rgb(25, 27, 31);"> 输出推理过程，并基于输入生成一组输出。</font>

```python
imag 1
A:<think>卡车有一个可以打开的门，在车的右边...</think>
..
imag n
Q：<think>这朵花似乎是哥伦比亚花，有五个黄色花瓣...</think><answer>哥伦比亚花</answer>
```

3. <font style="color:rgb(25, 27, 31);">每个响应通过</font>**<font style="color:rgb(25, 27, 31);">可验证奖励函数</font>**<font style="color:rgb(25, 27, 31);">计算奖励（</font>**<font style="color:#ED740C;">判断输出是否正确，给出打分评价</font>**<font style="color:rgb(25, 27, 31);">）。</font>
    1. <font style="color:rgb(25, 27, 31);">DeepSeek-R1 模型通过可验证奖励设计，在模型的推理能力上取得了显著提升。为了将这一策略转移到视觉领域，我们</font>**<font style="color:#ED740C;">为各种视觉感知任务设计了不同的基于规则的可验证奖励函数</font>**<font style="color:rgb(25, 27, 31);">。</font>
    2. **<font style="color:rgb(25, 27, 31);">检测任务中的交并比（IoU）奖励。IoU 奖励（RIoU）</font>**<font style="color:rgb(25, 27, 31);">：是模型输出中所有边界框的平均 IoU</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335260714-164fb956-d8f2-411e-94cb-7da4a40c2ed7.png)

    3. **<font style="color:rgb(25, 27, 31);">分类任务中的分类奖励（CLS Reward）：</font>**<font style="color:rgb(25, 27, 31);">在分类任务中，我们使用的奖励函数包含两部分：准确率奖励 Racc 和格式奖励 Rformat。准确率奖励通过比较模型输出的类别与真实类别来确定，正确分类得 1 分，错误分类得 0 分</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335300737-e056e0e2-782d-4b40-ae5e-667298eb1546.png)

4. <font style="color:rgb(25, 27, 31);">在对每个输出进行群体奖励计算后，评估每个响应的质量，并用于更新策略模型。</font>
    1. <font style="color:rgb(25, 27, 31);">为了确保策略模型训练的稳定性，Visual-RFT 使用</font>**<font style="color:rgb(25, 27, 31);"> KL 散度</font>**<font style="color:rgb(25, 27, 31);"> 限制策略模型与参考模型之间的差异。</font>

:::color5
**<font style="color:#601BDE;">4.数据准备</font>**

:::

<font style="color:rgb(25, 27, 31);">为了在各种视觉感知任务上训练 Visual-RFT，我们需要构建多模态训练数据集。与 DeepSeek-R1 类似，为了增强模型的推理能力，并将其应用于提升视觉感知能力，Visual-RFT </font>**<font style="color:#ED740C;">设计了一种提示格式，引导模型在输出最终答案之前</font>****<font style="color:#DF2A3F;">展示其推理过程（think)</font>**<font style="color:rgb(25, 27, 31);">。检测和分类任务中使用的提示格式如表 1 所示。</font>

1. **Detection Prompt**![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335490603-c16cf0e3-8ff4-43a8-bf25-9a0a133c37d1.png)**2. Classification Prompt**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741335496202-114105e4-f520-4fa0-985d-5ef63ebdd0e0.png)

:::color5
**<font style="color:#601BDE;">5.效果评估</font>**

:::

<font style="color:rgb(25, 27, 31);">广泛的实验表明，Visual-RFT 在细粒度分类、开放词汇检测、推理定位和少样本学习任务中表现出色。它</font>**<font style="color:rgb(25, 27, 31);">在数据量极少的情况下优于监督微调（SFT）</font>**<font style="color:rgb(25, 27, 31);">，并展现出强大的泛化能力。这项工作展示了强化学习增强 LVLMs 能力的潜力，使它们在视觉感知任务中更加高效和有效。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741333444294-84ba8e29-f966-451c-97b2-1ead9476673f.png)



## VLM-R1
:::color3
**<font style="color:rgb(51, 51, 51);">简介：</font>**<font style="color:rgb(25, 27, 31);">VLM-R1 是一款基于强化学习技术的视觉语言模型，能够通过自然语言指令精确定位图像目标，并支持多模态推理。  
</font><font style="color:rgb(25, 27, 31);">1. </font>**<font style="color:rgb(25, 27, 31);">指代表达理解</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精准定位图像中的特定目标。  
</font><font style="color:rgb(25, 27, 31);">2. </font>**<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：采用 </font>[<font style="color:rgb(9, 64, 142);">GRPO</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=GRPO&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 技术，在复杂场景下表现出色，提升泛化能力。</font>

**<font style="color:rgb(25, 27, 31);">github</font>**<font style="color:rgb(25, 27, 31);">:</font>[https://github.com/om-ai-lab/VLM-R1](https://github.com/om-ai-lab/VLM-R1)

:::

<font style="color:rgb(25, 27, 31);">VLM-R1 是浙江大学 Om AI Lab 开发的一款基于强化学习技术的视觉语言模型，旨在通过自然语言指令精确定位图像中的目标物体。例如，用户可以通过描述“图中红色的杯子”来让模型找到对应的图像区域。该模型基于 </font>[**<font style="color:rgb(9, 64, 142);">Qwen2.5-VL</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=Qwen2.5-VL&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 架构，结合了 </font>[**<font style="color:rgb(9, 64, 142);">DeepSeek R1</font>**](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=DeepSeek+R1&zhida_source=entity)<font style="color:rgb(25, 27, 31);"> 的强化学习方法，通过强化学习优化和监督微调（SFT）提升了模型的稳定性和泛化能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741316928362-b7a08f1d-fce8-4952-9b64-fd2b9fd5bc27.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">GRPO 强化学习技术</font>**<font style="color:rgb(25, 27, 31);">：</font>**<font style="color:#74B602;">采用 Group Relative Policy Optimization（GRPO）方法</font>**<font style="color:rgb(25, 27, 31);">，使模型在复杂场景下自我探索，减少对大量标注数据的依赖。</font>
+ **<font style="color:rgb(25, 27, 31);">泛化能力与稳定性提升</font>**<font style="color:rgb(25, 27, 31);">：相比传统的监督微调（SFT）方法，VLM-R1 在领域外测试数据中表现出持续提升的性能，表明其真正掌握了视觉内容的理解能力，而不仅仅是依赖记忆。</font>
+ **<font style="color:rgb(25, 27, 31);">基于 Qwen2.5-VL 架构</font>**<font style="color:rgb(25, 27, 31);">：在 Qwen2.5-VL 的基础上开发，通过强化学习优化，在多种复杂场景中保持稳定和高效的性能。</font>

:::color5
**<font style="color:#601BDE;">2.主要功能</font>**

:::

+ **<font style="color:rgb(25, 27, 31);">指代表达理解（REC）</font>**<font style="color:rgb(25, 27, 31);">：解析自然语言指令，精确定位图像中的特定目标，如根据描述“图中红色的杯子”找到对应区域。</font>
+ **<font style="color:rgb(25, 27, 31);">图像与文本联合处理</font>**<font style="color:rgb(25, 27, 31);">：支持同时输入图像和文字，生成准确的分析结果。</font>
+ **<font style="color:rgb(25, 27, 31);">强化学习优化</font>**<font style="color:rgb(25, 27, 31);">：通过 GRPO（Group Relative Policy Optimization）技术，提升模型在复杂场景下的表现和泛化能力。</font>
+ **<font style="color:rgb(25, 27, 31);">高效训练与推理</font>**<font style="color:rgb(25, 27, 31);">：采用 Flash Attention 等技术，支持单 GPU 训练大规模参数模型，提升计算效率。</font>
+ **<font style="color:rgb(25, 27, 31);">多模态推理与知识生成</font>**<font style="color:rgb(25, 27, 31);">：不仅能识别图像内容，还能进行逻辑推理和文本表达，例如识别蛋白质含量最高的食物并解释原因。</font>
+ **<font style="color:rgb(25, 27, 31);">易用性与开源性</font>**<font style="color:rgb(25, 27, 31);">：提供完整的训练和评估流程，开发者可以快速上手，四步即可开始训练。</font>

:::color5
**<font style="color:#601BDE;">3.GRPO在VLM中怎么做</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">如何迁移到多模态的疑问</font>**<font style="color:rgb(25, 27, 31);">：r1是用的规则奖励函数，而vlm的训练数据，很多是这种格式的： q + image -> a，那vlm是怎么跟r1结合到一起的？ 所以笔者去瞧了瞧，简单分享下这个项目是怎么把grpo迁移到vlm上的。</font>
2. **system prompt**

```yaml
用户和助手之间的对话。用户提出问题，助手解决问题。助手“首先在脑海中思考推理过程，然后为用户提供答案。推理”“过程和答案分别包含在<think></think>和<answer></answer>标签中，即“<think>推理过程在这里</hthink><answer>回答在这里</sanswer>”
```

2. **GRPO prompt**

```yaml
“｛Question｝首先在<think></think>标签中输出思考过程，然后在<answer></answer>标签中输入最终答案。以JSON格式输出最终答案。”
```

3. **奖励函数**

<font style="color:rgb(25, 27, 31);">一个格式奖励函数，一个IOU</font>[<font style="color:rgb(9, 64, 142);">函数</font>](https://zhida.zhihu.com/search?content_id=254040458&content_type=Article&match_order=1&q=iou%E5%87%BD%E6%95%B0&zhida_source=entity)<font style="color:rgb(25, 27, 31);">。IOU是目标检测中一个常见的度量标准， 简单来说两个框的交集面积除以并集面积的比值。判断是否大于0.5，给予奖励。</font>

<font style="color:rgb(25, 27, 31);">数据构造：把那个描述构造成问题，然后让模型预测框框的位置，这样就可以写出规则奖励函数了。</font>

```yaml
Question = “请提供输入语言描述区域的bounding box。”
```

:::color5
**<font style="color:#601BDE;">4.评测</font>**

:::

<font style="color:rgb(25, 27, 31);">左图是测试相同领域评测结果，右图是out-of-domain的评测结果。随着训练步骤增加，grpo相比sft都有明显优势，sft更容易过拟合。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741317431287-e98b46f9-ddce-440a-9669-528ca28d4a8d.png)

:::color5
**<font style="color:#601BDE;">5.如何运行VLM-R1</font>**

:::

1. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">环境搭建</font>**

<font style="color:rgb(25, 27, 31);">在开始运行 VLM-R1 模型之前，需要配置运行环境。以下是环境搭建的步骤：</font>

```plain
conda create -n vlm-r1 python=3.10
conda activate vlm-r1
bash setup.sh
```

<font style="color:rgb(25, 27, 31);">通过上述命令，创建并激活一个名为 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">vlm-r1</font>`<font style="color:rgb(25, 27, 31);"> 的 Python 环境，并运行 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">setup.sh</font>`<font style="color:rgb(25, 27, 31);"> 脚本来安装依赖。</font>

2. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">数据准备</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 模型的训练需要准备图像数据和标注文件。以下是数据准备的详细步骤：</font>

**<font style="color:rgb(25, 27, 31);">(1)下载图像数据</font>**

<font style="color:rgb(25, 27, 31);">下载</font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">COCO Train2014</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=COCO+Train2014&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">图像数据</font>`<font style="color:rgb(25, 27, 31);">并解压，将图像文件夹路径记为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"><your_image_root></font>`<font style="color:rgb(25, 27, 31);">。</font>

+ **<font style="color:rgb(25, 27, 31);">COCO Train2014 图像数据</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://huggingface.co/datasets/omlab/VLM-R1/resolve/main/train2014.zip](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/omlab/VLM-R1/resolve/main/train2014.zip)

**<font style="color:rgb(25, 27, 31);">(2)下载标注文件</font>**

<font style="color:rgb(25, 27, 31);">下载</font>`[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">RefCOCO/+</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=RefCOCO%2F%2B&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">/g 和</font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font>[<font style="color:rgb(9, 64, 142);background-color:rgb(248, 248, 250);">RefGTA</font>](https://zhida.zhihu.com/search?content_id=254299792&content_type=Article&match_order=1&q=RefGTA&zhida_source=entity)<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);"> </font><font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">标注文件</font>`<font style="color:rgb(25, 27, 31);">并解压。RefGTA 用于域外评估。</font>

+ **<font style="color:rgb(25, 27, 31);">RefCOCO/+/g 和 RefGTA 标注文件</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://huggingface.co/datasets/omlab/VLM-R1/resolve/main/rec_jsons_processed.zip](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/omlab/VLM-R1/resolve/main/rec_jsons_processed.zip)

**<font style="color:rgb(25, 27, 31);">(3) 配置标注文件路径</font>**

<font style="color:rgb(25, 27, 31);">在</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">src/open-r1-multimodal/data_config/rec.yaml</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">文件中，填写标注文件的路径。例如：</font>

```plain
datasets:
    - json_path: /path/to/refcoco_train.json
    - json_path: /path/to/refcocop_train.json
    - json_path: /path/to/refcocog_train.json
```

3. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">模型训练</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 提供了两种训练方法：GRPO 和 SFT。以下是两种方法的详细步骤。</font>

**<font style="color:rgb(25, 27, 31);">(1) GRPO 方法</font>**

<font style="color:rgb(25, 27, 31);">运行以下命令以启动 GRPO 方法的训练：</font>

```plain
cd src/open-r1-multimodal

torchrun --nproc_per_node="8" \
    --nnodes="1" \
    --node_rank="0" \
    --master_addr="127.0.0.1" \
    --master_port="12346" \
    src/open_r1/grpo_rec.py \
    --deepspeed local_scripts/zero3.json \
    --output_dir output/$RUN_NAME \
    --model_name_or_path Qwen/Qwen2.5-VL-3B-Instruct \
    --dataset_name data_config/rec.yaml \
    --image_root <your_image_root> \
    --max_prompt_length 1024 \
    --num_generations 8 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 2 \
    --logging_steps 1 \
    --bf16 \
    --torch_dtype bfloat16 \
    --data_seed 42 \
    --report_to wandb \
    --gradient_checkpointing false \
    --attn_implementation flash_attention_2 \
    --num_train_epochs 2 \
    --run_name $RUN_NAME \
    --save_steps 100 \
    --save_only_model true
```

<font style="color:rgb(25, 27, 31);">如果遇到</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">CUDA out of memory</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">错误，可以尝试以下方法： 1. 设置</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">gradient_checkpointing</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">为</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">true</font>`<font style="color:rgb(25, 27, 31);">。 2. 减少</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">num_generations</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的值。 3. 使用 LoRA 方法。</font>

**<font style="color:rgb(25, 27, 31);">(2) SFT 方法</font>**

<font style="color:rgb(25, 27, 31);">首先，克隆</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory</font>`<font style="color:rgb(25, 27, 31);">仓库并安装依赖：</font>

+ **<font style="color:rgb(25, 27, 31);">LLaMA-Factory 仓库</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/hiyouga/LLaMA-Factory](https://link.zhihu.com/?target=https%3A//github.com/hiyouga/LLaMA-Factory)

```plain
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

<font style="color:rgb(25, 27, 31);">接着，下载提供的 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">dataset_info.json</font>`<font style="color:rgb(25, 27, 31);">、</font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">mllm_rec_json.json</font>`<font style="color:rgb(25, 27, 31);"> 和 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">qwen2_5_vl_full_sft.yaml</font>`<font style="color:rgb(25, 27, 31);"> 文件，分别放置在 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/data</font>`<font style="color:rgb(25, 27, 31);"> 和 </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">LLaMA-Factory/examples/train_full</font>`<font style="color:rgb(25, 27, 31);"> 目录中。</font>

<font style="color:rgb(25, 27, 31);">最后，运行以下命令以启动 SFT 方法的训练：</font>

```plain
llamafactory-cli train examples/train_full/qwen2_5_vl_full_sft.yaml
```

4. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">自定义数据支持</font>**

<font style="color:rgb(25, 27, 31);">VLM-R1 支持自定义数据的加载，数据格式需为 JSONL 文件。以下是数据格式示例：</font>

```plain
{"id": 1, "image": "Clevr_CoGenT_TrainA_R1/data/images/CLEVR_trainA_000001_16885.png", "conversations": [{"from": "human", "value": "<image>What number of purple metallic balls are there?"}, {"from": "gpt", "value": "0"}]}
```

**<font style="color:rgb(25, 27, 31);">(1) 注意事项</font>**

1. <font style="color:rgb(25, 27, 31);">JSONL 文件中的图像路径应为相对于</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">--image_folders</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">指定的文件夹路径。</font>
2. <font style="color:rgb(25, 27, 31);">多个数据文件和图像文件夹可以通过</font><font style="color:rgb(25, 27, 31);"> </font>`<font style="color:rgb(25, 27, 31);background-color:rgb(248, 248, 250);">:</font>`<font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">分隔。例如：</font>

```plain
--data_file_paths /path/to/data1.jsonl:/path/to/data2.jsonl \
--image_folders /path/to/images1/:/path/to/images2/
```

**<font style="color:rgb(25, 27, 31);">(2) 加载自定义数据</font>**

<font style="color:rgb(25, 27, 31);">运行以下命令以加载自定义数据：</font>

```plain
torchrun --nproc_per_node="8" \
    --nnodes="1" \
    --node_rank="0" \
    --master_addr="127.0.0.1" \
    --master_port="12345" \
  src/open_r1/grpo_jsonl.py \
    --output_dir output/$RUN_NAME \
    --model_name_or_path Qwen/Qwen2.5-VL-3B-Instruct \
    --deepspeed local_scripts/zero3.json \
    --dataset_name <your_dataset_name> \
    --data_file_paths /path/to/your/data.jsonl \
    --image_folders /path/to/your/image/folder/
```

5. **<font style="color:rgb(25, 27, 31);background-color:#D9EAFC;">模型评估</font>**

<font style="color:rgb(25, 27, 31);">模型训练完成后，可以使用以下命令进行评估：</font>

```plain
cd ./src/eval

# 修改脚本中的模型路径、图像根目录和标注文件路径
python test_rec_r1.py # 用于 GRPO 方法
python test_rec_baseline.py # 用于 SFT 方法
```



## Vision-R1
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">近两年，大模型（LLM）在各个领域大放异彩，从语言理解到图像识别，都出现了突破性的进展。然而，想要</font>**<font style="color:#117CEE;">让模型真正地“像人一样”去进行推理、思考与解释，仍是一项极富挑战性的任务</font>**<font style="color:rgb(25, 27, 31);">。以往我们大多在文本领域探索如何“让模型有自己的思维过程”（如链式思考 Chain-of-Thought），而在多模态领域（尤其是图文结合的情境）——如何把</font>**<font style="color:#117CEE;">视觉信息与语言信息进行深度融合并激发复杂的推理能力</font>**<font style="color:rgb(25, 27, 31);">，还远远没有走到头。</font>

<font style="color:rgb(25, 27, 31);">为此，本文针对多模态大模型（Multimodal LLM，简称 MLLM）的“推理能力激发”展开研究，并提出了一个全新的解决方案，名为</font><font style="color:#74B602;"> </font>**<font style="color:#74B602;">Vision-R1</font>**<font style="color:#74B602;">。</font>**<font style="color:#74B602;">它在视觉和语言的结合中，实现了用“强化学习（RL）+ 冷启动（Cold Start）”的方式，去让模型自发地产生更复杂、更类似于人类思考的推理链。</font>**

:::

:::color3
**简介：****<font style="color:#117CEE;">仅靠强化学习（RL）无法有效激励多模态大型语言模型（MLLM）的推理能力，主要原因是缺乏高质量初始数据和优化策略。</font>**<font style="color:rgb(25, 27, 31);">Vision-R1 提出了一条“冷启动+强化学习”相结合的训练路径，为多模态大模型（MLLM）注入类人式思维与推理能力。具体而言，</font>**<font style="color:#74B602;">先通过“模态桥接（Modality Bridging）”方法大规模生成高质量多模态推理数据并进行冷启动初始化</font>**<font style="color:rgb(25, 27, 31);">；随后利用</font>**<font style="color:#74B602;">渐进式思维抑制训练（</font>**[**<font style="color:#74B602;">PTST</font>**](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=PTST&zhida_source=entity)**<font style="color:#74B602;">）与强化学习相结合</font>**<font style="color:rgb(25, 27, 31);">，逐步引导模型掌握正确且复杂的推理过程。实验表明，Vision-R1-7B 参数规模的模型便能在多项数理推理基准上逼近甚至超越 70B+ 大模型的表现。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/Osilly/Vision-R1](https://github.com/Osilly/Vision-R1)

**paper：**[**Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models**](https://arxiv.org/pdf/2503.06749)

**参考：**[**https://zhuanlan.zhihu.com/p/29618155786**](https://zhuanlan.zhihu.com/p/29618155786)

:::

:::color5
**<font style="color:#601BDE;">1.研究动机</font>**

:::

<font style="color:rgb(25, 27, 31);">1.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">语言大模型的推理火热，但多模态推理仍是短板</font>**

<font style="color:rgb(25, 27, 31);">近年来，纯文本领域的推理方法（如“链式思考”、Tree-of-Thought 等）发展迅速，证明了在文本任务中，通过显式的多步推理，可以极大提升模型在复杂问题上的表现。然而，这些方法大多只聚焦在文字输入上，很少考虑视觉信息。</font>**<font style="color:#117CEE;">多模态模型若只停留在“根据图像简单识别+给出答案”，常常难以在高难度推理场景（如数学场景的图文结合推理、几何题带图解等）表现优异</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">2.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">直接用强化学习在多模态模型上激发“自发思考”并不容易</font>**

<font style="color:rgb(25, 27, 31);">在纯文本模型上，已有工作（如 DeepSeek-R1）表明，利用强化学习去激发模型自我生成更复杂的推理链，确实有效。但想</font>**<font style="color:#117CEE;">直接将这种强化学习方法“照搬”到多模态模型，会面临数据稀缺、模型过度胡乱生成长推理链等问题，导致效果不佳</font>**<font style="color:rgb(25, 27, 31);">。因此，需要一个辅助的冷启动初始化步骤来帮助模型先学会“如何思考”，然后再进行强化学习，以提升推理过程的正确性与稳健性。</font>

<font style="color:rgb(25, 27, 31);">3.</font><font style="color:rgb(25, 27, 31);"> </font>**<font style="color:rgb(25, 27, 31);">缺乏大规模高质量多模态推理数据</font>**

<font style="color:rgb(25, 27, 31);">人工标注的图文推理数据往往只包含简单的“图像描述+答案”，很少显式写出内在的思考过程，即便有也通常比较“形式化”，缺乏像人类一样的“自我质疑”“多步检验”。</font>**<font style="color:#117CEE;">如何构建能体现“人类式推理”的多模态数据，是推动 MLLM 学习复杂推理的关键</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">目标：</font>**

+ <font style="color:rgb(25, 27, 31);">生成高质量的多模态推理链（CoT）数据集，无需人工标注。</font>
+ <font style="color:rgb(25, 27, 31);">通过 RL 优化模型，使其生成逻辑清晰、长度适中的 CoT，避免过度思考（Overthinking）。</font>

:::color5
**<font style="color:#601BDE;">2.Vision-R1 pipeline</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610218132-f1874efd-d72a-49ba-891b-e93a78d70d58.png)

Vision-R1流程。首先利用现有的MLLM和[DeepSeek-R1](https://zhida.zhihu.com/search?content_id=254946168&content_type=Article&match_order=1&q=DeepSeek-R1&zhida_source=entity)获得高质量的Multimodal CoT数据集，将其作为基础MLLM的冷启动初始化数据，从而得到经过冷启动后的Vision-R1-CI，然后在Vision-R1-CI上进行强化学习（RL）训练，最终获得具备推理能力的MLLM，即Vision-R1。  
	我们观察到，直接在MLLM上应用RL无法有效地激发出强大的推理能力（参见(C)和(D)）。未经初始化直接通过RL训练的Vision-R1-Zero难以从有限的数据中泛化（参见(E)、(F)，特别指出Vision-R1-Zero应用了format reward function）。而Vision-R1-CI则面临“过度思考优化问题（Overthinking Optimization Problem）”，偏好较短的CoT推理序列，即正确的推理过程主要集中在较短的CoT推理序列中（参见(A)）。在后续的RL训练中，我们观察到推理步骤虽然有所延长，但性能却出现下降（参见(D)和(E)），这使得优化尤为困难。而Vision-R1则首先在RL训练下缩短CoT，以精炼正确的思考过程。PTST使Vision-R1逐步获得更为复杂的推理过程（参见(C)、(D)和(E)），性能得以提升，因此我们的Vision-R1以70亿参数实现了与具有700亿以上参数的最强MLLM相当的性能（参见(B)）。注意，Vision-R1使用了不同颜色的线条来表示PTST中的不同阶段。

:::color5
**<font style="color:#601BDE;">3.数据合成pipeline</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744610119279-268e2a66-4fdd-4e72-b86c-68c3ced7a91e.png)

整体的数据生成流程，融合了我们的模态桥接（Modality Bridging）方法。首先将多模态数据送入MLLM，以获取包含图像描述（caption）和推理过程的“Pseudo-CoT”，并将其与原始的图像-问题对一起作为MLLM的输入，以生成详细的文本描述。通过这种模态桥接方法，文本描述向DeepSeek-R1提供了全面的信息，有助于生成高质量的CoT推理过程。这些推理过程经过后处理，与原始数据整合后，最终形成Vision-R1-cold数据集。

**实现细节**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612056366-1bd3e083-a561-4989-9b82-c378f09ddb9e.png)

1. **<font style="color:rgb(25, 27, 31);">伪CoT生成</font>**<font style="color:rgb(25, 27, 31);">：首先，使用现有的多模态大型语言模型（MLLM）来生成“伪CoT”（Pseudo-CoT）。具体的，输入一个图像-问题-答案对和一个提示到一个MLLM中，模型会生成一个包含图像描述和推理过程的文本。这个“伪CoT”不仅包含了图像的描述，还尝试进行初步的推理，但可能缺乏深度和复杂性。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744612131128-77febf08-96d2-4f16-aee8-f64fdf6888c8.png)

2. **<font style="color:rgb(25, 27, 31);">文本描述生成</font>**<font style="color:rgb(25, 27, 31);">：将生成的“伪CoT”与原始的图像-问题对以及一个新的提示一起输入到同一个MLLM中，以获取更详细的图像描述。这一步骤的目的是通过MLLM的文本生成能力，将图像中的视觉信息转化为更详细的文本描述，从而为后续的推理提供更多的上下文信息。</font>
3. **<font style="color:rgb(25, 27, 31);">推理生成</font>**<font style="color:rgb(25, 27, 31);">：将经过文本化的图像-问题对输入到一个专门的推理大型语言模型（如</font>**<font style="color:rgb(25, 27, 31);">DeepSeek-R1</font>**<font style="color:rgb(25, 27, 31);">）中，以生成高质量的CoT推理过程。DeepSeek-R1能够生成包含自然认知过程的推理过程，如质疑、反思和检查等。</font>
4. **<font style="color:rgb(25, 27, 31);">数据过滤</font>**<font style="color:rgb(25, 27, 31);">：从生成的CoT数据中保留那些最终答案与真实值一致的样本。使用规则进行数据过滤，去除逻辑不一致的样本，并替换一些词汇以提高语义连贯性。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法：渐进式思维抑制训练（PTST）</font>**

:::

<font style="color:rgb(25, 27, 31);">为了解决冷启动后的过度思考问题，Vision-R1 采用渐进式思维抑制训练（PTST），通过 RL 进一步优化模型的推理能力。</font>

+ **<font style="color:rgb(25, 27, 31);">分组相对策略优化（GRPO）：</font>**<font style="color:rgb(25, 27, 31);"> GRPO 是一种 RL 算法，通过分组类似状态或动作来优化策略，提高学习效率。 详细的可参考往期《</font>[DeepSeek采用的GRPO算法数学原理及算法过程浅析](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg4NjI0NDg0Ng%3D%3D%26mid%3D2247487491%26idx%3D1%26sn%3De3e2c5a43b107c16b12a0bfcd0c0de75%26chksm%3Dcf9dc482f8ea4d94a382afa4903869f0d3ffe660dfaeae2e71e50fcc580b30e1bced687622c9%26scene%3D178%26cur_album_id%3D2829992858538491905%23rd)<font style="color:rgb(25, 27, 31);">》</font>
+ **<font style="color:rgb(25, 27, 31);">硬格式结果奖励函数（HFRRF）：</font>**<font style="color:rgb(25, 27, 31);"> 奖励函数简单：如果输出格式正确且答案正确，则奖励为 1，否则为 0。</font>
+ **<font style="color:rgb(25, 27, 31);">分阶段训练：</font>**<font style="color:rgb(25, 27, 31);"> 训练分为多个阶段，逐步增加序列长度（如 4K、8K、16K 标记）和调整组大小（如 16、8、4）。</font>
    - <font style="color:rgb(25, 27, 31);">每个阶段训练 100 步，使用 64 个 </font>[<font style="color:rgb(9, 64, 142);">NVIDIA H800 80G GPU</font>](https://zhida.zhihu.com/search?content_id=255000916&content_type=Article&match_order=1&q=NVIDIA+H800+80G+GPU&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，约 2 天，使用 Verl 框架。</font>
    - <font style="color:rgb(25, 27, 31);">与固定长度 16K、300 步训练的 Vision-R1-Long 相比，PTST 表现更好，平均长度 2057，平均准确率 55.4%。</font>

:::color5
**<font style="color:#601BDE;">5.评估</font>**

:::

**<font style="color:rgb(25, 27, 31);">1. 效果对比</font>**

<font style="color:rgb(25, 27, 31);">• 在多项数理推理（包含图文几何推理、方程推导等）基准上，Vision-R1-7B 尺度的模型，已经能与一些 70B+ 参数的大模型旗鼓相当。例如，在 MathVista、MathVerse、MM-Math 等基准上，Vision-R1-7B 都取得了显著提升，</font>**<font style="color:rgb(25, 27, 31);">在MathVista上，Vision-R1-7B 73.5分，接近OpenAI o1的73.9</font>**<font style="color:rgb(25, 27, 31);">。 某些子任务（如几何推理）甚至逼近或超越现有最优水平。</font>

<font style="color:rgb(25, 27, 31);">• 说明只要</font>**<font style="color:#74B602;">“冷启动 + 强化学习”得当，中小参数量的多模态模型，也能产生相当强的推理能力</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">2. 人类式思维过程的可观测性</font>**

<font style="color:rgb(25, 27, 31);">• 论文中展示了 Vision-R1 的多步推理示例，能看到模型在回答一个几何题时，会出现类似人类的“嗯？我再检查一下”“好像上一步有点问题，让我再重新推一下”等</font>**<font style="color:#74B602;">自我质疑、思考的字句</font>**<font style="color:rgb(25, 27, 31);">。</font>

<font style="color:rgb(25, 27, 31);">• 这表明在训练中确实</font>**<font style="color:#74B602;">激发了模型的“自发思考”模式</font>**<font style="color:rgb(25, 27, 31);">，而不仅仅是机械地输出一长串无效的步骤。</font>

**<font style="color:rgb(25, 27, 31);">3. 渐进训练的优势</font>**

<font style="color:rgb(25, 27, 31);">• 实验还对比了如果没有分阶段抑制推理长度，模型要么推理很短（零强化学习），要么推理超长但正确率显著下降（直接用 16K tokens 长度训练）。</font>**<font style="color:#74B602;">通过“逐步放宽推理长度”的方式，能帮助 Vision-R1 获得优质的平衡</font>**<font style="color:rgb(25, 27, 31);">：既能长推理，又不至于陷入胡乱瞎想的陷阱。</font>

:::color5
**<font style="color:#601BDE;">6.总结 & 展望</font>**

:::

**<font style="color:rgb(25, 27, 31);">总结：Vision-R1</font>**<font style="color:rgb(25, 27, 31);"> 的工作提供了一个有意思的思路：</font>

<font style="color:rgb(25, 27, 31);">• 首先利用已有多模态模型与高质量文本推理模型，通过“模态桥接”构造大量“人类式思维”的数据，为 MLLM 做一个冷启动；</font>

<font style="color:rgb(25, 27, 31);">• 再通过严格的奖励设计和分阶段策略，在强化学习中逐步激发更高级的推理链。</font>

<font style="color:rgb(25, 27, 31);">从实验结果看，这样的技术路线能显著提升多模态模型在复杂推理任务（尤其是图文结合数学推理）上的表现，也为后续大模型如何结合视觉、语言并启用更深层次思考提供了新思路。</font>

**<font style="color:rgb(25, 27, 31);">未来思考：</font>**

<font style="color:rgb(25, 27, 31);">1. 模型能否迁移到视频、三维、以及更多模态的复杂推理场景？</font>

<font style="color:rgb(25, 27, 31);">2. 是否可以结合其他RL算法比如DAPO、VAPO以及多模态PRM来进一步稳定强化学习过程，并提升性能上限？</font>

<font style="color:rgb(25, 27, 31);">3. 如何让多模态推理不仅有“解释可读性”，还要兼顾“鲁棒性”和“正确性”，尤其减少模型产生的不合理自我纠正和幻觉？</font>

<font style="color:rgb(25, 27, 31);">尽管还有很多问题值得探索，但 Vision-R1 的研究已经为“多模态大模型的深层推理”这条赛道，注入了新的可能性与动力。</font>

## Video-R1
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">当前的多模态大模型（MLLMs）在处理视频时存在一个根本性问题：</font>**<font style="color:#117CEE;">它们往往无法有效利用视频中的时序信息</font>**<font style="color:rgb(25, 27, 31);">。想象一下，如果你只看电影的几个随机截图，而不是按顺序观看整部电影，你能理解剧情吗？显然不能。但这正是当前多模态大模型的工作方式——它们更像是在处理一系列独立的图像，而非真正理解视频中的时序变化。</font>

<font style="color:rgb(25, 27, 31);">另一个挑战是</font>**<font style="color:#117CEE;">高质量视频推理数据的稀缺</font>**<font style="color:rgb(25, 27, 31);">。现有的视频数据集主要集中在简单的识别任务上，缺乏需要复杂推理能力的数据，这使得模型很难学习到真正的视频推理能力。</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">为了解决这些问题，研究团队提出了两个创新方案。（1）</font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。（2）针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。</font>

**<font style="color:rgb(25, 27, 31);">项目地址</font>**<font style="color:rgb(25, 27, 31);">：</font>[https://github.com/tulerfeng/Video-R1](https://github.com/tulerfeng/Video-R1)

**paper：**[**Video-R1: Reinforcing Video Reasoning in MLLMs**](https://arxiv.org/pdf/2503.21776)

**参考：**[**https://zhuanlan.zhihu.com/p/1889342435928282728**](https://zhuanlan.zhihu.com/p/1889342435928282728)

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602200071-763ca10e-6dd5-42bc-bae9-f7fe62dcee02.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

1. **<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于</font>**<font style="color:#74B602;">鼓励模型进行时序推理</font>**<font style="color:rgb(25, 27, 31);">。</font>
2. <font style="color:rgb(25, 27, 31);">针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>
    1. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>
    2. <font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

:::color5
**<font style="color:#601BDE;">2.T-GRPO算法（Temporal Group Relative Policy Optimization，时序群组相对策略优化）</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744601979834-580a4129-df2b-4699-afe6-57c9e06d78fb.png)

<font style="color:rgb(25, 27, 31);"></font>**<font style="color:rgb(25, 27, 31);">T-GRPO算法</font>**<font style="color:rgb(25, 27, 31);">（Temporal Group Relative Policy Optimization，时序群组相对策略优化）。这是对原有GRPO算法的扩展，专门设计用于鼓励模型进行时序推理。</font>

**<font style="color:rgb(25, 27, 31);">T-GRPO的核心思想非常巧妙</font>**<font style="color:rgb(25, 27, 31);">：在训练过程中，模型会同时处理</font>**<font style="color:#74B602;">两种视频输入</font>**<font style="color:#74B602;">——</font>**<font style="color:#74B602;">按时间顺序排列的帧序列和随机打乱的帧序列</font>**<font style="color:rgb(25, 27, 31);">。如果模型在有序序列上的表现优于乱序序列，它就会获得正向奖励。这种对比机制有效地鼓励模型利用帧间的时序关系进行推理，而不是仅仅依赖于单帧图像中的视觉特征。</font>

:::color5
**<font style="color:#601BDE;">3.训练数据</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602073812-c3c90af5-55aa-4f9a-8600-1549f9e496a2.png)

<font style="color:rgb(25, 27, 31);">其次，针对高质量视频推理数据稀缺的问题，研究团队采取了一种混合训练策略，</font>**<font style="color:#74B602;">巧妙地引入图像推理数据作为训练数据的一部分</font>**<font style="color:rgb(25, 27, 31);">。他们构建了两个数据集：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-COT-165k</font>**<font style="color:rgb(25, 27, 31);">：用于监督微调（SFT）的数据集，包含具有思维链（Chain-of-Thought）注释的图像和视频样本。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">Video-R1-260k</font>**<font style="color:rgb(25, 27, 31);">：用于强化学习（RL）训练的数据集，包含多种类型的图像和视频推理任务。</font>

<font style="color:rgb(25, 27, 31);">这种混合训练方式使模型能够从图像中学习到基础推理技能，再将这些技能迁移到视频领域，从而有效克服了视频推理数据稀缺的问题。</font>

:::color5
**<font style="color:#601BDE;">4.评估</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1744602107401-1ffbcfd1-715c-4fd7-ab34-a8db348ea124.png)

<font style="color:rgb(25, 27, 31);">研究团队在多个视频理解和推理基准测试上评估了Video-R1的性能，结果令人印象深刻：</font>

**<font style="color:rgb(25, 27, 31);">在VSI-Bench（一个视频空间推理基准测试）上，Video-R1-7B达到了35.8%的准确率，超越了商业专有模型GPT-4o</font>**<font style="color:rgb(25, 27, 31);">，而它仅使用了32帧输入和7B参数。这一结果凸显了显式推理能力在解决视频任务中的必要性。</font>

<font style="color:rgb(25, 27, 31);">研究还发现，在强化学习阶段，即使只进行了1000步训练，Video-R1的性能也显著提升，特别是在推理密集型任务上。这清楚地表明了该强化学习框架的效力，并强调了强化学习在释放可泛化视频推理能力方面的重要性。</font>

<font style="color:rgb(25, 27, 31);">此外，当增加输入帧数从16到32时，模型在几乎所有基准测试上的性能都有所提高。这表明更长的上下文和更丰富的时序信息对模型的推理性能有积极贡献。</font>

:::color5
**<font style="color:#601BDE;">5.未来方向</font>**

:::

<font style="color:rgb(25, 27, 31);">尽管Video-R1取得了令人瞩目的成果，但研究团队也指出了几个限制和未来的研究方向：</font>

<font style="color:rgb(25, 27, 31);">（1）</font>**<font style="color:rgb(25, 27, 31);">增加帧数</font>**<font style="color:rgb(25, 27, 31);">：当前模型使用16个视频帧训练，这可能限制其处理长时序依赖的能力。未来可以开发更高效的训练和推理策略，以处理更长的视频。</font>

<font style="color:rgb(25, 27, 31);">（2）</font>**<font style="color:rgb(25, 27, 31);">更好的时序建模方法</font>**<font style="color:rgb(25, 27, 31);">：虽然T-GRPO引入了有效的时序感知推理，但它带来了额外的计算开销。未来可以通过探索更高效的时序建模机制来缓解这一问题。</font>

<font style="color:rgb(25, 27, 31);">（3）</font>**<font style="color:rgb(25, 27, 31);">动态响应长度控制</font>**<font style="color:rgb(25, 27, 31);">：当前的长度控制机制在预定义范围内应用固定奖励，而不考虑每个样本的复杂性。未来工作可以探索动态长度控制策略。</font>

<font style="color:rgb(25, 27, 31);">（4）</font>**<font style="color:rgb(25, 27, 31);">大规模强化学习</font>**<font style="color:rgb(25, 27, 31);">：受计算资源限制，当前的强化学习阶段仅训练了1000步。尽管结果很有希望，但增加强化学习训练规模可能会进一步提高模型性能。</font>

<font style="color:rgb(25, 27, 31);">（5）</font>**<font style="color:rgb(25, 27, 31);">改进图像到视频的知识迁移</font>**<font style="color:rgb(25, 27, 31);">：目前，研究团队以直接混合的方式将图像推理数据纳入训练集。未来研究可以设计更有原则的方法，更有效地将推理能力从图像迁移到视频。</font>





<font style="color:rgb(25, 27, 31);"></font>

## MM-RLHF<font style="color:#D22D8D;"></font>
:::success
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(25, 27, 31);">尽管</font>[<font style="color:rgb(9, 64, 142);">多模态大语言模型</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81%E5%A4%A7%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B&zhida_source=entity)<font style="color:rgb(25, 27, 31);">（</font>[<font style="color:rgb(9, 64, 142);">MLLMs</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=MLLMs&zhida_source=entity)<font style="color:rgb(25, 27, 31);">）取得了显著的进展，但现有的先进模型仍然缺乏与人类偏好的充分对齐。这一差距的存在主要是因为现有的对齐研究多集中于某些特定领域（例如减少幻觉问题），</font>**<font style="color:rgb(25, 27, 31);">是否与人类偏好对齐可以全面提升MLLM的各种能力</font>**<font style="color:rgb(25, 27, 31);">仍是一个未知数。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

:::

:::color3
**简介：**<font style="color:rgb(25, 27, 31);">快手，</font>[<font style="color:rgb(9, 64, 142);">中科院</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E4%B8%AD%E7%A7%91%E9%99%A2&zhida_source=entity)<font style="color:rgb(25, 27, 31);">，</font>[<font style="color:rgb(9, 64, 142);">南大</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=%E5%8D%97%E5%A4%A7&zhida_source=entity)<font style="color:rgb(25, 27, 31);">合作从三个层面入手推动MLLM alignment的发展，包括数据集，奖励模型以及训练算法，最终的alignment pipeline使得不同基础模型在</font>**<font style="color:rgb(25, 27, 31);">10</font>**<font style="color:rgb(25, 27, 31);">个评估维度，</font>**<font style="color:rgb(25, 27, 31);">27</font>**<font style="color:rgb(25, 27, 31);">个benchmark上都取得了一致的性能增益，比较突出的是，基于本文提出的数据集和对齐算法对LLaVA-ov-7B模型进行微调后， conversational 能力平均提升了 </font>**<font style="color:rgb(25, 27, 31);">19.5</font>**<font style="color:rgb(25, 27, 31);">%，安全性平均提升了 </font>**<font style="color:rgb(25, 27, 31);">60</font>**<font style="color:rgb(25, 27, 31);">%。</font><font style="color:#D22D8D;">（by草莓师姐）</font>

<font style="color:rgb(25, 27, 31);">[</font>[arXiv Paper](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2502.10391)<font style="color:rgb(25, 27, 31);">] [</font>[Training Code](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/MM-RLHF)<font style="color:rgb(25, 27, 31);">] [</font>[Homepage](https://link.zhihu.com/?target=https%3A//mm-rlhf.github.io/)<font style="color:rgb(25, 27, 31);">] [</font>[Reward Model](https://link.zhihu.com/?target=https%3A//huggingface.co/yifanzhang114/MM-RLHF-Reward-7B-llava-ov-qwen)<font style="color:rgb(25, 27, 31);">] [</font>[MM-RewardBench](https://link.zhihu.com/?target=https%3A//huggingface.co/datasets/yifanzhang114/MM-RLHF-RewardBench)<font style="color:rgb(25, 27, 31);">] [</font>[MM-SafetyBench](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/mmrlhf-eval)<font style="color:rgb(25, 27, 31);">] [</font>[Evaluation Suite](https://link.zhihu.com/?target=https%3A//github.com/yfzhang114/mmrlhf-eval)<font style="color:rgb(25, 27, 31);">]</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281079377-8d72cdcf-f88f-4e6d-9b17-918c2f58595a.png)

> MM-RLHF pipeline。（1）数据收集和清理：从1000万个指令样本开始，我们根据图像相似性对数据进行聚类，并在不同类别中统一采样。这导致了一个多样化的数据集，涵盖了基于图像的问答（例如，多项选择题、对话和安全相关问题）和视频问答格式。（2）响应生成：我们利用最先进的模型，包括GPT-4o和Qwen2-VL-72B，生成高质量的响应。（3）人工标注：我们对评分、排名和解释等九个类别进行人工标注，确保细粒度评估。
>

:::color5
**<font style="color:#601BDE;">1.主要贡献</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(25, 27, 31);">新数据集</font>**<font style="color:rgb(25, 27, 31);">：本文引入了一个</font>**<font style="color:#74B602;">包含 120k 精细标注的偏好比较对的数据集</font>**<font style="color:rgb(25, 27, 31);">，包含三个维度的打分，排序，文本描述的具体原因以及平局等标注，</font>**<font style="color:rgb(25, 27, 31);">所有标注由人类专家完成</font>**<font style="color:rgb(25, 27, 31);">，一共</font>**<font style="color:rgb(25, 27, 31);">50</font>**<font style="color:rgb(25, 27, 31);">名标注人员，</font>**<font style="color:rgb(25, 27, 31);">8</font>**<font style="color:rgb(25, 27, 31);">名专家，耗时两个月。与现有资源相比，这一数据集在规模、样本多样性、标注粒度和质量等方面都有显著提升。</font>
2. **<font style="color:rgb(25, 27, 31);">创新的奖励模型</font>**<font style="color:rgb(25, 27, 31);">：提出了 </font>**<font style="color:rgb(25, 27, 31);">基于批评的奖励模型（</font>**[**<font style="color:rgb(9, 64, 142);">Critique-Based Reward Model</font>**](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=Critique-Based+Reward+Model&zhida_source=entity)**<font style="color:rgb(25, 27, 31);">）</font>**<font style="color:rgb(25, 27, 31);">，该模型</font>**<font style="color:#74B602;">首先对模型输出进行批评，然后再进行评分</font>**<font style="color:rgb(25, 27, 31);">。这一方法相比传统的标量奖励机制，提供了更好的可解释性和更有信息量的反馈，基于该方法的模型只需要7B size，在reward model benchmark就明显优于现有公开的72B-size的MLLM。</font>
3. **<font style="color:rgb(25, 27, 31);">动态奖励缩放</font>**<font style="color:rgb(25, 27, 31);">：提出了 </font>**<font style="color:rgb(25, 27, 31);">动态奖励缩放（Dynamic Reward Scaling）</font>**<font style="color:rgb(25, 27, 31);"> 方法，通过</font>**<font style="color:#74B602;">根据奖励信号调整每个样本的损失权重</font>**<font style="color:rgb(25, 27, 31);">，优化了高质量比较对的使用，进一步提高了数据的使用效率。</font>
4. **<font style="color:rgb(25, 27, 31);">全面评估</font>**<font style="color:rgb(25, 27, 31);">：本文在 </font>**<font style="color:rgb(25, 27, 31);">10</font>**<font style="color:rgb(25, 27, 31);"> 个维度和 </font>**<font style="color:rgb(25, 27, 31);">27</font>**<font style="color:rgb(25, 27, 31);"> 个基准上对提出的方案进行了严格评估，同时构</font>**<font style="color:rgb(25, 27, 31);">造了一个reward model的benchmark以及safety相关的benchmark</font>**<font style="color:rgb(25, 27, 31);">来弥补现有benchmark的不足，结果显示，在各个方面均取得了显著且一致的性能提升。</font>

:::color5
**<font style="color:#601BDE;">2.人类偏好数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281079377-8d72cdcf-f88f-4e6d-9b17-918c2f58595a.png)

1. **<font style="color:rgb(25, 27, 31);">数据来源</font>**<font style="color:rgb(25, 27, 31);">：图像数据来源包括 LLaVA-OV、VLfeedback、LLaVA-RLHF、lrv-instruction 和 Unimm-Chat 等，总共10M，视频数据来源主要是SharedGPT-4-video，安全性相关的数据来源主要包括 VLGuard 和自构造内容。</font>
2. **<font style="color:rgb(25, 27, 31);">数据过滤与模型响应生成</font>**<font style="color:rgb(25, 27, 31);">，通过预定义的多选题，长文本等类别均匀采样，确保少数类也有足够的样本。同时采用了knn聚类并采样的策略，保证数据的diversity。响应生成使用到了Qwen2-VL-72B、LLaVA-OV-72B、GPT-4o 和 Claude 3.5-sonnet等最先进的MLLM。</font>
3. **<font style="color:rgb(25, 27, 31);">数据标注</font>**<font style="color:rgb(25, 27, 31);">：主要包含三个维度，</font>**<font style="color:#74B602;">有用性，真实性，伦理性</font>**<font style="color:rgb(25, 27, 31);">，同时标注人员需要提供打分的依据，最终排名以及排名的依据，标注粒度细，通过专家定期进行质量检查和互动评审保证标注质量。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747280981149-2b807f48-430b-4f14-99e0-3e7db0184123.png)

> 重新采样聚类过程的结果。由于样本总数庞大，聚类和重复数据消除的结果包含丰富多样的类别。选定的样本包括数学、日常生活、自然场景、医学、电子技术和OCR场景等主题，展示了各种问题图像对。通过UMAP降维获得二维特征。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281040828-0b34cb89-d63a-4fef-99d3-8dd407096c67.png)

> 数据集组成统计
>

:::color5
**<font style="color:#601BDE;">3.MM-RLHF奖励模型</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281259360-ef3ea49f-af34-4f75-9719-3b2c340a9de5.png)

> 多任务奖励模型训练过程的说明。该过程从用户查询和相应的模型响应开始，由人类对其进行排名和注释。使用GPT-4o扩展人类注释，以提供增强的理由。奖励模型的训练有两个目标：（1）学习提供批评，模型学习为模型响应提供详细的批评和评估，以及（2）学习评分，模型学习根据模型响应和批评分配分数。这些任务的整合确保了改进模型输出的稳健评估框架。
>

<font style="color:rgb(25, 27, 31);">标准奖励模型通常通过预训练的LLM，</font>**<font style="color:#74B602;">并用线性奖励头替换原有头部，以输出一个标量奖励值</font>**<font style="color:rgb(25, 27, 31);">。然而，这些模型</font>**<font style="color:#117CEE;">难以充分利用人类注释中的丰富信息，也不具备足够的透明性</font>**<font style="color:rgb(25, 27, 31);">。  
</font><font style="color:rgb(25, 27, 31);">	为了解决标准奖励模型的局限性，本文提出了一种基于批评的训练框架。在这个框架中，</font>**<font style="color:#74B602;">模型首先生成批评（对响应的分析和评估），然后基于批评来打分</font>**<font style="color:rgb(25, 27, 31);">。批评生成部分与打分部分共同作用，确保了更细致的评价。</font>

**<font style="color:rgb(25, 27, 31);">增强注释以提高批评质量</font>**<font style="color:rgb(25, 27, 31);">：由于人工注释往往简洁且精炼，直接使用它们作为训练目标效果有限。因此，本文通过</font>**<font style="color:#74B602;">GPT-4o增强人工注释，使其更为详细和流畅</font>**<font style="color:rgb(25, 27, 31);">，从而提高批评的质量。</font>

<font style="color:rgb(25, 27, 31);">在训练过程中，批评的生成与奖励头的训练同时进行，在训练奖励头时采取了teacher-forcing的策略，即采用了ground truth的批评作为输入，默认损失权重都为1。</font>**<font style="color:#74B602;">测试阶段先生成批评，然后基于批评得出最终得分。</font>**

:::color5
**<font style="color:#601BDE;">4.性能评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281506594-b7fd651f-0251-4121-bfa1-cdf9af3ad3dc.png)

> MM RLHF RewardBench上指标和方法的性能比较。MM RLHF奖励（不包括任务1）表示训练LLaVA-OV-7B模型对成对样本进行评分，同时排除任务1。MM RLHF奖励（不含增强注释）涉及学习人类提供的注释，然后进行评分。MM RLHF奖赏（推理含GT注释）在推理过程中使用基本事实注释。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747281512868-c874bb58-a23a-44b5-a717-8b8372490397.png)

> 我们的奖励模型（MM RLHF奖励）与现有的开源和私有多模式模型的性能比较。MM-RLHF-Reward-7B的性能优于现有的72B开源多模态模型和几个竞争激烈的闭源模型。
>

<font style="color:rgb(25, 27, 31);">该模型框架简单，且在多个基准测试中的表现与GPT-4o相媲美，甚至超越了许多开源模型，表现出色，尤其在自定义基准测试中，其表现远超GPT-4o，这验证了其作为训练算法奖励信号的有效性。</font>

<font style="color:rgb(25, 27, 31);">表4中也展示了，当奖励头直接使用偏好数据集进行训练时，模型的ACC+稳定在50%左右。然而，当引入人工注释作为学习目标时，ACC+稳定提升了5%。进一步通过GPT-4o扩展人工注释，生成更加详细和流畅的批评，最终提高了ACC+达17%。当评估时直接使用人工批评时，ACC和ACC+均接近90%，表明评估质量对奖励模型效果的至关重要性。</font>

:::color5
**<font style="color:#601BDE;">5.MM-DPO：有效利用高质量偏好数据</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747288984946-f690c128-154e-471f-88e6-71fa1572e3e2.png)

<font style="color:rgb(25, 27, 31);">要有效利用MM-RLHF中的高质量数据，我们有以下的实验发现和技巧</font>

1. **<font style="color:rgb(25, 27, 31);">MM-DPO不再仅仅关注“最难的比较对”（即排名差异最大的一对）</font>**<font style="color:rgb(25, 27, 31);">，而是将一个查询下所有可能的响应对都纳入训练。具体来说，对于一个查询</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">x</font><font style="color:rgb(25, 27, 31);">，如果有多个响应，每一对具有不同排名的响应都被视为一个有效的比较对。这种全面的处理方式可以捕捉更细粒度的排序信息，让模型从更广泛的偏好数据中学习。然</font>**<font style="color:rgb(25, 27, 31);">而，这种策略也带来了新的挑战</font>**<font style="color:rgb(25, 27, 31);">：当响应对的排名差异较小时（例如排名 3 和排名 4 的比较），其奖励差距（reward margin）往往较小，而排名差异较大的响应对（例如排名 1 和排名 4 的比较）包含的信息质量更高。如果对所有样本对一视同仁，会导致高置信度的信息被低效利用。  
</font>
2. <font style="color:rgb(25, 27, 31);">为了解决这个问题，MM-DPO 引入了动态奖励缩放（Dynamic Reward Scaling）机制，根据奖励差距动态调整更新强度，优先利用高置信度的样本对。具体而言，奖励模型可以自然地为样本对提供奖励差距（reward margin），这为动态控制样本的更新权重提供了一个直接的信号。</font>

<font style="color:rgb(25, 27, 31);">本文采用MM-RLHF-Reward-7B 模型来计算奖励差距</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">=</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">−</font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);">,</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">其中</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">和</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">r</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">y</font><font style="color:rgb(25, 27, 31);">l</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">分别是正样本和负样本的奖励分数。</font>

<font style="color:rgb(25, 27, 31);">DPO中，动态缩放因子</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">(</font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">)</font><font style="color:rgb(25, 27, 31);"> </font><font style="color:rgb(25, 27, 31);">的计算公式如下：</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289224985-0d1f7e92-0259-45f2-821d-32247d66094f.png)

<font style="color:rgb(25, 27, 31);">其中：</font><font style="color:rgb(25, 27, 31);">βori</font><font style="color:rgb(25, 27, 31);"> 是初始默认缩放因子;</font><font style="color:rgb(25, 27, 31);">w</font><font style="color:rgb(25, 27, 31);"> 是一个参数，用于平衡动态部分的贡献；</font><font style="color:rgb(25, 27, 31);">k</font><font style="color:rgb(25, 27, 31);"> 是一个可调超参数，控制 </font><font style="color:rgb(25, 27, 31);">β(δ)</font><font style="color:rgb(25, 27, 31);">随着</font><font style="color:rgb(25, 27, 31);">δ</font><font style="color:rgb(25, 27, 31);">的变化速度。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289030103-ba37aa55-f407-497e-920b-110b978feb63.png)

<font style="color:rgb(25, 27, 31);">接下来只需要将DPO算法中的</font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">部分替换为动态的</font><font style="color:rgb(25, 27, 31);">β</font><font style="color:rgb(25, 27, 31);">即可。</font>

<font style="color:rgb(25, 27, 31);">MM-DPO在各类benchmark上都表现出了不错的性能增益，而且其对于超参数并不是非常敏感，大多数情况下都能使得高质量pair的利用效率得到明显提升。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747289269736-7dc58805-2244-4e0d-b626-4cc7f5c90955.png)

> 对我们的方法和数据集进行消融研究。（a）现实世界任务评估，其中“LLaVA-OV-7B”作为基线模型，“+MM-RLHF”表示我们的数据集与传统DPO算法的结合使用。“+隐性奖励”是指在LLM中使用动态贝塔策略[65]。（b）评估超参数k和w对MM-DPO模型的影响，证明这些变化对排行榜得分的影响。
>

:::color5
**<font style="color:#601BDE;">6.27个评估标准，10种评估维度的综合评估</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">主要领域包括图表与文档理解、OCR、幻觉检测、数学推理、通用知识、多模态对话、高分辨率与真实世界应用、视频理解、多图像处理以及多模态安全性。其中，多模态安全性基准 MM-RLHF-SafeBench 是自构建的，涵盖对抗攻击、越狱攻击、隐私保护和有害内容生成等场景，重点评估模型的安全性与鲁棒性。这些数据集为模型的多方面性能提供了详尽的测试环境。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747292757393-103cc9b4-b08a-48df-8af0-151373d40b11.png)

> 在8个不同的评估维度上对齐后的性能变化，比较我们对齐策略下的多个模型。所有模型在拟议的对齐下都显示出全面的性能改进，表明在各种任务中都取得了显著成果。
>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1747292812501-defdd4cb-dbd9-4445-a691-5806ad2b96f1.png)

> MM RLHF SafeBench校准后的性能变化，比较我们的对齐策略下的多个模型。
>

<font style="color:rgb(25, 27, 31);">上面两图展示了使用我们的数据集和对齐算法，LLaVA-OV-7B、LLaVA-OV-0.5B和InternVL-1B在不同维度上的对齐表现，其中每个评估维度的得分在相应的基准上进行了平均。</font>

**<font style="color:rgb(25, 27, 31);">会话能力和安全性的显著提升</font>**<font style="color:rgb(25, 27, 31);">： 实验结果表明，通过对齐过程，这两个方面的表现得到了显著改进，无需调整超参数。在会话基准中，平均提高超过10%，而不安全行为减少了至少50%。此外，在</font>[<font style="color:rgb(9, 64, 142);">WildsVision</font>](https://zhida.zhihu.com/search?content_id=253872299&content_type=Article&match_order=1&q=WildsVision&zhida_source=entity)<font style="color:rgb(25, 27, 31);">任务中，胜率至少提高了50%。</font>

**<font style="color:rgb(25, 27, 31);">在幻觉、数学推理、多图像和视频理解方面的广泛提升</font>**<font style="color:rgb(25, 27, 31);">： 对齐后的模型在这些领域表现出显著的提升。有趣的是，尽管我们的数据集中缺乏专门的多图像数据，模型在多图像任务中的表现依然显著提升。这表明我们数据集的多样性有助于模型在多个维度上进行更好的泛化。</font>

:::color5
**<font style="color:#601BDE;">7.未来方向</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(25, 27, 31);">在本研究中，我们提出了MM-RLHF，一个高质量、细粒度的数据集，专门用于推动多模态大语言模型（MLLMs）的对齐工作。与以往专注于特定任务的研究不同，我们的数据集和对齐方法旨在全面提升多个维度的性能。即使在奖励建模和优化算法方面仅进行了初步改进，我们在几乎所有评估基准上都观察到了显著且持续的提升，强调了综合性对齐策略的潜力。</font>

<font style="color:rgb(25, 27, 31);">展望未来，我们看到进一步挖掘我们数据集价值的巨大机会。数据集的丰富注释粒度，如每个维度的分数和排名理由，在当前的对齐算法中仍未得到充分利用。未来的工作将重点关注利用这些粒度信息与先进的优化技术，结合高分辨率数据来解决特定基准的局限性，并使用半自动化策略高效地扩展数据集。我们相信，这些努力不仅将推动MLLM对齐到新的高度，还将为更广泛、更具普适性的多模态学习框架奠定基础。</font>



