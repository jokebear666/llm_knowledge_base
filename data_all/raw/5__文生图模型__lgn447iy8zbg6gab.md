# 5️⃣ 文生图模型

<!-- source: yuque://zhongxian-iiot9/hlyypb/lgn447iy8zbg6gab -->

# 文生图
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">文生图（Text-to-Image）模型能够根据文本描述生成对应图像，近年来在生成对抗网络（GAN）、变分自编码器（VAE）和扩散模型（Diffusion Models）等技术推动下快速发展。以下是主要模型及其原理、实现和应用</font>

:::

| **模型** | **核心技术** | **开源** | **分辨率** | **训练成本** | **优点** | **缺点** |
| --- | --- | --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">Stable Diffusion</font> | <font style="color:rgb(51, 51, 51);">潜在扩散模型</font> | <font style="color:rgb(51, 51, 51);">是</font> | <font style="color:rgb(51, 51, 51);">512x512</font> | <font style="color:rgb(51, 51, 51);">中等</font> | <font style="color:rgb(51, 51, 51);">开源、高效</font> | <font style="color:rgb(51, 51, 51);">文本对齐依赖数据质量</font> |
| <font style="color:rgb(51, 51, 51);">DALL-E 3</font> | <font style="color:rgb(51, 51, 51);">扩散+GPT-4</font> | <font style="color:rgb(51, 51, 51);">否</font> | <font style="color:rgb(51, 51, 51);">1024x1024</font> | <font style="color:rgb(51, 51, 51);">极高</font> | <font style="color:rgb(51, 51, 51);">复杂提示词支持</font> | <font style="color:rgb(51, 51, 51);">闭源、生成慢</font> |
| <font style="color:rgb(51, 51, 51);">Imagen</font> | <font style="color:rgb(51, 51, 51);">级联扩散</font> | <font style="color:rgb(51, 51, 51);">否</font> | <font style="color:rgb(51, 51, 51);">1024x1024</font> | <font style="color:rgb(51, 51, 51);">极高</font> | <font style="color:rgb(51, 51, 51);">高分辨率生成</font> | <font style="color:rgb(51, 51, 51);">计算成本高</font> |
| <font style="color:rgb(51, 51, 51);">MidJourney</font> | <font style="color:rgb(51, 51, 51);">专有扩散</font> | <font style="color:rgb(51, 51, 51);">否</font> | <font style="color:rgb(51, 51, 51);">动态调整</font> | <font style="color:rgb(51, 51, 51);">高</font> | <font style="color:rgb(51, 51, 51);">用户友好、风格多样</font> | <font style="color:rgb(51, 51, 51);">黑盒、不可控</font> |


**开源说明**

+ **<font style="color:rgb(51, 51, 51);">Stable Diffusion</font>**<font style="color:rgb(51, 51, 51);">：完整训练代码需定义VAE、UNet和调度器（参考</font>[diffusers库](https://github.com/huggingface/diffusers)<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">DALL-E/Imagen</font>**<font style="color:rgb(51, 51, 51);">：因未开源，建议使用官方API或参考论文复现（如</font>[MinDALL-E](https://github.com/kakaobrain/mindallee)<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">MidJourney</font>**<font style="color:rgb(51, 51, 51);">：无公开代码，需通过Discord调用。</font>

# <font style="color:rgba(0, 0, 0, 0.9);">阿里云</font><font style="color:rgb(15, 89, 164);">视觉生成基座模型万相2.1（Wan）</font>
[https://mp.weixin.qq.com/s/o_F06JzKq72V1UBudQCbuw](https://mp.weixin.qq.com/s/o_F06JzKq72V1UBudQCbuw)

# <font style="color:rgb(51, 51, 51);">Stable Diffusion</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Stable Diffusion原理</font>

+ <font style="color:rgb(51, 51, 51);">基于</font>**<font style="color:rgb(51, 51, 51);">潜在扩散模型（Latent Diffusion Model, LDM）</font>**<font style="color:rgb(51, 51, 51);">，通过将图像压缩到低维潜在空间进行扩散过程，降低计算复杂度。</font>
+ <font style="color:rgb(51, 51, 51);">结合</font>**<font style="color:rgb(51, 51, 51);">CLIP文本编码器</font>**<font style="color:rgb(51, 51, 51);">，将文本描述映射到潜在空间指导生成。</font>
+ <font style="color:rgb(51, 51, 51);">扩散过程分两步：</font>
    1. **<font style="color:rgb(51, 51, 51);">前向过程（加噪）</font>**<font style="color:rgb(51, 51, 51);">：逐步向数据中添加高斯噪声。</font>
    2. **<font style="color:rgb(51, 51, 51);">反向过程（去噪）</font>**<font style="color:rgb(51, 51, 51);">：通过神经网络预测噪声，逐步恢复图像。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">编码阶段</font>**<font style="color:rgb(51, 51, 51);">:</font><font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">c</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">CLIP_Text_Encoder</font><font style="color:rgb(51, 51, 51);">(</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">e</font><font style="color:rgb(51, 51, 51);">x</font><font style="color:rgb(51, 51, 51);">t</font><font style="color:rgb(51, 51, 51);">)</font><font style="color:rgb(51, 51, 51);">=</font><font style="color:rgb(51, 51, 51);">CLIP_Text_Encoder</font><font style="color:rgb(51, 51, 51);">(</font>_<font style="color:rgb(51, 51, 51);">t</font>__<font style="color:rgb(51, 51, 51);">e</font>__<font style="color:rgb(51, 51, 51);">x</font>__<font style="color:rgb(51, 51, 51);">t</font>_<font style="color:rgb(51, 51, 51);">)</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);">。</font>
    - <font style="color:rgb(51, 51, 51);">VAE将图像编码到潜在空间：z=VAE_Encoder(x)。</font>
1. **<font style="color:rgb(51, 51, 51);">扩散过程</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">正向过程：逐步添加噪声 q(zt∣zt−1)。</font>
    - <font style="color:rgb(51, 51, 51);">反向过程：通过UNet预测噪声 ϵθ(zt,t,c)，其中 c</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 是文本条件。</font>
2. **<font style="color:rgb(51, 51, 51);">解码阶段</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">VAE解码器将潜在变量 z0</font>_<font style="color:rgb(51, 51, 51);"></font>_<font style="color:rgb(51, 51, 51);"> 恢复为图像：x=VAE_Decoder(z0)。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算高效（在潜在空间操作）。</font>
    - <font style="color:rgb(51, 51, 51);">生成质量高，支持细粒度控制。</font>
    - <font style="color:rgb(51, 51, 51);">开源社区支持丰富（如Hugging Face</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);">diffusers</font>`<font style="color:rgb(51, 51, 51);">库）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">对复杂文本提示的解析仍有局限。</font>
    - <font style="color:rgb(51, 51, 51);">需要大量训练数据。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">艺术创作、广告设计、游戏素材生成。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">ControlNet</font>**<font style="color:rgb(51, 51, 51);">：引入额外条件（如边缘检测图）控制生成细节。</font>
+ **<font style="color:rgb(51, 51, 51);">LoRA</font>**<font style="color:rgb(51, 51, 51);">：低秩适配器微调，提升模型对特定风格的学习能力。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "A futuristic cityscape at sunset"
image = pipe(prompt).images[0]
image.save("output.png")

```

# VAE
<font style="color:rgb(51, 51, 51);">VAE (Variational Autoencoder) 模型详解</font>

:::color3
**背景：**

**<font style="color:rgb(51, 51, 51);">生成模型需求</font>**<font style="color:rgb(51, 51, 51);">：传统自编码器（AE）难以生成新数据，因隐空间缺乏结构化约束。</font>  
**<font style="color:rgb(51, 51, 51);">概率建模发展</font>**<font style="color:rgb(51, 51, 51);">：变分推断（VI）提供了一种在隐变量模型中近似后验分布的方法。</font>  
**<font style="color:rgb(51, 51, 51);">VAE定位</font>**<font style="color:rgb(51, 51, 51);">：Kingma等提出的生成模型，结合神经网络与变分推断，实现可学习的隐变量分布与高效采样。</font>

:::

<font style="color:rgb(51, 51, 51);">VAE通过变分推断与重参数化技巧，为生成模型提供了概率框架。尽管生成质量不及GAN，但其稳定训练和隐空间解释性优势明显。后续改进模型（如VQ-VAE、NVAE）通过结构优化显著提升了生成能力。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741094075658-8adb4e77-9adb-4d15-9841-f3f6b46d0f6c.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">变分下界（ELBO）</font>**<font style="color:rgb(51, 51, 51);">：通过最大化证据下界近似数据对数似然。</font>
+ **<font style="color:rgb(51, 51, 51);">重参数化技巧</font>**<font style="color:rgb(51, 51, 51);">：使梯度可通过随机隐变量传播，解决采样不可导问题。</font>
+ **<font style="color:rgb(51, 51, 51);">隐空间正则化</font>**<font style="color:rgb(51, 51, 51);">：强制隐变量分布接近标准正态分布（KL散度约束）。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">无标注数据</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像：MNIST、CIFAR-10、CelebA等。</font>
    - <font style="color:rgb(51, 51, 51);">非图像数据：文本、音频、分子结构等。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像归一化到[0,1]或[-1,1]。</font>
    - <font style="color:rgb(51, 51, 51);">文本需转换为词嵌入或序列编码。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">编码器（推理网络）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：数据样本x（如图像）。</font>
    - <font style="color:rgb(51, 51, 51);">输出：隐变量z的后验分布参数（μ, logσ²）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：CNN（图像）或MLP（非图像）。</font>
+ **<font style="color:rgb(51, 51, 51);">隐变量采样</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">z = μ + ε⊙exp(0.5*logσ²)，其中ε∼N(0,I)。</font>
+ **<font style="color:rgb(51, 51, 51);">解码器（生成网络）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">输入：隐变量z。</font>
    - <font style="color:rgb(51, 51, 51);">输出：重构数据x̂ 的分布参数（如Bernoulli均值）。</font>
    - <font style="color:rgb(51, 51, 51);">结构：反卷积网络（图像）或MLP。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741094135342-a50a601c-2b2c-400a-88a9-d260897947bb.png)

1. **前向过程**：
    - <font style="color:rgb(51, 51, 51);">编码器输出q(z|x)的参数μ, σ。</font>
    - <font style="color:rgb(51, 51, 51);">重参数化采样z。</font>
    - <font style="color:rgb(51, 51, 51);">解码器输出p(x|z)的参数。</font>
2. **损失计算**：
    - **<font style="color:rgb(51, 51, 51);">重构损失</font>**<font style="color:rgb(51, 51, 51);">：如交叉熵（二分类数据）或MSE（连续数据）。</font>
    - **<font style="color:rgb(51, 51, 51);">KL散度</font>**<font style="color:rgb(51, 51, 51);">：KL(q(z|x) || N(0,I))。</font>
    - **<font style="color:rgb(51, 51, 51);">总损失</font>**<font style="color:rgb(51, 51, 51);">：L = 重构损失 + β*KL散度（β-VAE变体）。</font>
3. **反向传播**：
    - <font style="color:rgb(51, 51, 51);">通过梯度下降同时优化编码器和解码器。</font>
4. **生成新样本**：
    - <font style="color:rgb(51, 51, 51);">从N(0,I)采样z，输入解码器生成x̂。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">可生成新样本，隐空间具有插值特性。</font>
+ <font style="color:rgb(51, 51, 51);">提供概率解释，支持不确定性建模。</font>
+ <font style="color:rgb(51, 51, 51);">端到端训练，无需马尔可夫链采样。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">生成样本可能模糊（尤其图像）。</font>
+ <font style="color:rgb(51, 51, 51);">KL散度项可能导致隐变量坍缩（部分维度失效）。</font>
+ <font style="color:rgb(51, 51, 51);">难以建模复杂分布（需改进先验或后验形式）。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据生成</font>**<font style="color:rgb(51, 51, 51);">：图像、文本、分子结构合成。</font>
+ **<font style="color:rgb(51, 51, 51);">特征学习</font>**<font style="color:rgb(51, 51, 51);">：无监督特征提取用于下游任务。</font>
+ **<font style="color:rgb(51, 51, 51);">异常检测</font>**<font style="color:rgb(51, 51, 51);">：低重构概率标识异常样本。</font>
+ **<font style="color:rgb(51, 51, 51);">半监督学习</font>**<font style="color:rgb(51, 51, 51);">：结合少量标注数据提升分类性能。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">β-VAE</font>**<font style="color:rgb(51, 51, 51);">：调整KL项权重（β>1）以提升解耦表示。</font>
+ **<font style="color:rgb(51, 51, 51);">VQ-VAE</font>**<font style="color:rgb(51, 51, 51);">：引入矢量量化层离散化隐空间。</font>
+ **<font style="color:rgb(51, 51, 51);">CVAE</font>**<font style="color:rgb(51, 51, 51);">：条件VAE，通过额外信息（如类别）控制生成。</font>
+ **<font style="color:rgb(51, 51, 51);">NVAE</font>**<font style="color:rgb(51, 51, 51);">：层级化隐变量与深度神经网络提升生成质量。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):
    def __init__(self, input_dim, hidden_dim, latent_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
    
    def forward(self, x):
        h = F.relu(self.fc1(x))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

class Decoder(nn.Module):
    def __init__(self, latent_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(latent_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, z):
        h = F.relu(self.fc1(z))
        recon = torch.sigmoid(self.fc2(h))
        return recon

class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=400, latent_dim=20):
        super().__init__()
        self.encoder = Encoder(input_dim, hidden_dim, latent_dim)
        self.decoder = Decoder(latent_dim, hidden_dim, input_dim)
    
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def forward(self, x):
        mu, logvar = self.encoder(x.view(-1, 784))
        z = self.reparameterize(mu, logvar)
        recon_x = self.decoder(z)
        return recon_x, mu, logvar

# 训练函数
def train(model, dataloader, optimizer, device):
    model.train()
    train_loss = 0
    for batch_idx, (data, _) in enumerate(dataloader):
        data = data.to(device)
        optimizer.zero_grad()
        recon_batch, mu, logvar = model(data)
        
        # 计算重构损失和KL散度
        BCE = F.binary_cross_entropy(recon_batch, data.view(-1, 784), reduction='sum')
        KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        
        loss = BCE + KLD
        loss.backward()
        train_loss += loss.item()
        optimizer.step()
    return train_loss / len(dataloader.dataset)

# 示例调用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vae = VAE().to(device)
optimizer = torch.optim.Adam(vae.parameters(), lr=1e-3)

# 训练循环
for epoch in range(10):
    loss = train(vae, train_loader, optimizer, device)
    print(f'Epoch {epoch}, Loss: {loss:.2f}')

# 生成新样本
with torch.no_grad():
    z = torch.randn(64, 20).to(device)
    samples = vae.decoder(z).view(64, 1, 28, 28)

```



# <font style="color:rgb(51, 51, 51);">DALL-E系列（DALL-E 2/3）</font>
## <font style="color:rgb(51, 51, 51);">DALL·E</font>
:::color3
**<font style="color:rgb(51, 51, 51);">背景</font>**<font style="color:rgb(51, 51, 51);">：</font>

**<font style="color:rgb(51, 51, 51);">文本到图像生成需求</font>**<font style="color:rgb(51, 51, 51);">：传统图像生成方法（如GAN）难以精确对齐复杂文本描述，且缺乏跨模态理解能力。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">多模态突破</font>**<font style="color:rgb(51, 51, 51);">：GPT系列验证了自回归模型在文本生成中的潜力，需将其扩展到视觉领域。</font><font style="color:rgb(51, 51, 51);">  
</font>**<font style="color:rgb(51, 51, 51);">DALL·E定位</font>**<font style="color:rgb(51, 51, 51);">：OpenAI提出的首个大规模文本到图像自回归模型，实现从开放域文本描述生成高质量图像。</font>

:::

<font style="color:rgb(51, 51, 51);">DALL·E通过自回归建模实现文本到图像的突破性生成，其核心在于将图像离散化并与文本联合建模。后续工作（如DALL·E 2）引入扩散模型进一步提升质量，但初代模型仍具有重要方法论价值。未来方向包括提升生成效率、增强细粒度控制等。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741093616375-38b5b954-c4fe-4d81-a247-769de1b34981.png)

:::color5
**<font style="color:#601BDE;">1.创新点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像离散化表示</font>**<font style="color:rgb(51, 51, 51);">：通过离散VAE将图像压缩为token序列，实现文本与图像的联合建模。</font>
+ **<font style="color:rgb(51, 51, 51);">多模态自回归架构</font>**<font style="color:rgb(51, 51, 51);">：将文本和图像token拼接，使用Transformer建模联合分布。</font>
+ **<font style="color:rgb(51, 51, 51);">零样本生成能力</font>**<font style="color:rgb(51, 51, 51);">：无需特定类别微调，直接根据新文本描述生成图像。</font>
+ **<font style="color:rgb(51, 51, 51);">两阶段训练流程</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">阶段1</font>**<font style="color:rgb(51, 51, 51);">：训练离散VAE压缩图像。</font>
    - **<font style="color:rgb(51, 51, 51);">阶段2</font>**<font style="color:rgb(51, 51, 51);">：训练自回归Transformer生成图像token序列。</font>

:::color5
**<font style="color:#601BDE;">2.训练数据</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">图像-文本对</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">来源：网络公开数据（如Conceptual Captions）+ 专有数据集。</font>
    - <font style="color:rgb(51, 51, 51);">规模：数亿级图文对（具体未公开）。</font>
+ **<font style="color:rgb(51, 51, 51);">文本多样性</font>**<font style="color:rgb(51, 51, 51);">：包含复杂场景描述（如"穿宇航服的猫在月球上弹吉他"）。</font>
+ **<font style="color:rgb(51, 51, 51);">预处理</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">图像统一分辨率（256x256或512x512）。</font>
    - <font style="color:rgb(51, 51, 51);">文本经BPE编码（与GPT-3共用词表）。</font>

:::color5
**<font style="color:#601BDE;">3.模型结构</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">离散VAE（dVAE）</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">编码器</font>**<font style="color:rgb(51, 51, 51);">：CNN将图像压缩为32x32的离散token（词表大小8192）。</font>
    - **<font style="color:rgb(51, 51, 51);">解码器</font>**<font style="color:rgb(51, 51, 51);">：CNN将token重建为图像。</font>
+ **<font style="color:rgb(51, 51, 51);">自回归Transformer</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - **<font style="color:rgb(51, 51, 51);">输入拼接</font>**<font style="color:rgb(51, 51, 51);">：文本token（256个） + 图像token（1024个）。</font>
    - **<font style="color:rgb(51, 51, 51);">架构</font>**<font style="color:rgb(51, 51, 51);">：类似GPT-3，使用稀疏注意力机制（128层，120亿参数）。</font>
    - **<font style="color:rgb(51, 51, 51);">位置编码</font>**<font style="color:rgb(51, 51, 51);">：学习式位置编码处理序列顺序。</font>

:::color5
**<font style="color:#601BDE;">4.训练方法</font>**

:::

1. **dVAE预训练**：
    - <font style="color:rgb(51, 51, 51);">目标：最小化重建损失（L2 + 感知损失）。</font>
    - <font style="color:rgb(51, 51, 51);">优化：Gumbel-Softmax松弛离散采样过程。</font>
2. **Transformer训练**：
    - <font style="color:rgb(51, 51, 51);">输入：文本token与对应图像的dVAE token拼接。</font>
    - <font style="color:rgb(51, 51, 51);">目标：最大化似然估计（交叉熵损失）。</font>
    - <font style="color:rgb(51, 51, 51);">策略：按文本长度动态调整注意力掩码。</font>
3. **CLIP辅助优化**（可选）：
    - <font style="color:rgb(51, 51, 51);">使用CLIP模型计算图像-文本相似度，指导生成方向。</font>

:::color5
**<font style="color:#601BDE;">5.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">开放域生成能力强大，支持复杂组合式描述。</font>
+ <font style="color:rgb(51, 51, 51);">零样本迁移无需额外训练。</font>
+ <font style="color:rgb(51, 51, 51);">生成图像与文本语义高度对齐。</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

+ <font style="color:rgb(51, 51, 51);">生成分辨率受限（通常256x256）。</font>
+ <font style="color:rgb(51, 51, 51);">自回归生成速度慢（需逐token预测）。</font>
+ <font style="color:rgb(51, 51, 51);">细节控制能力有限（如精确物体位置）。</font>

:::color5
**<font style="color:#601BDE;">6.应用场景</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">创意设计</font>**<font style="color:rgb(51, 51, 51);">：根据文案自动生成广告配图。</font>
+ **<font style="color:rgb(51, 51, 51);">艺术创作</font>**<font style="color:rgb(51, 51, 51);">：辅助画家实现抽象概念可视化。</font>
+ **<font style="color:rgb(51, 51, 51);">教育工具</font>**<font style="color:rgb(51, 51, 51);">：将历史事件描述转化为场景图像。</font>
+ **<font style="color:rgb(51, 51, 51);">产品原型</font>**<font style="color:rgb(51, 51, 51);">：快速生成设计草图供团队讨论。</font>

:::color5
**<font style="color:#601BDE;">7.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">混合架构</font>**<font style="color:rgb(51, 51, 51);">：结合扩散模型提升生成质量（如DALL·E 2）。</font>
+ **<font style="color:rgb(51, 51, 51);">层级式生成</font>**<font style="color:rgb(51, 51, 51);">：先生成低分辨率草图，再逐步细化。</font>
+ **<font style="color:rgb(51, 51, 51);">空间控制</font>**<font style="color:rgb(51, 51, 51);">：引入布局描述符（如边界框）指导物体位置。</font>
+ **<font style="color:rgb(51, 51, 51);">高效解码</font>**<font style="color:rgb(51, 51, 51);">：使用非自回归模型加速生成过程。</font>

:::color5
**<font style="color:#601BDE;">8.代码实现</font>**

:::

```python
import torch
import torch.nn as nn

class dVAE(nn.Module):
    def __init__(self, vocab_size=8192):
        super().__init__()
        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 64, 4, stride=2, padding=1),  # 128x128
            nn.ReLU(),
            nn.Conv2d(64, 128, 4, stride=2, padding=1), # 64x64
            nn.ReLU(),
            nn.Conv2d(128, 256, 4, stride=2, padding=1), # 32x32
            nn.ReLU(),
            nn.Conv2d(256, vocab_size, 1)  # 32x32x8192
        )
        # 解码器
        self.decoder = nn.Sequential(
            nn.Conv2d(vocab_size, 256, 1),  # 32x32x256
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1), # 64x64
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),  # 128x128
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, 4, stride=2, padding=1)     # 256x256
        )

    def encode(self, x):
        logits = self.encoder(x)  # [B, 8192, 32, 32]
        return torch.argmax(logits, dim=1)  # 离散token [B, 32, 32]

    def decode(self, tokens):
        one_hot = nn.functional.one_hot(tokens, 8192).float().permute(0,3,1,2)
        return self.decoder(one_hot)

```

```python
from transformers import GPT2LMHeadModel

class DALLETransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.gpt = GPT2LMHeadModel.from_pretrained("gpt2-xl")
        self.text_emb = nn.Embedding(50257, 1600)  # GPT-2词表
        self.image_emb = nn.Embedding(8192, 1600)  # dVAE词表
        
    def forward(self, text_ids, image_ids):
        # 嵌入拼接
        text_emb = self.text_emb(text_ids)  # [B, T_text, D]
        image_emb = self.image_emb(image_ids) # [B, T_image, D]
        inputs_emb = torch.cat([text_emb, image_emb], dim=1)
        # GPT前向
        outputs = self.gpt(inputs_embeds=inputs_emb)
        return outputs.logits

# 训练循环示例
dvae = dVAE()
transformer = DALLETransformer()
optimizer = torch.optim.Adam(transformer.parameters(), lr=1e-4)

for batch in dataloader:
    images, texts = batch
    # 编码图像为token
    with torch.no_grad():
        image_tokens = dvae.encode(images)  # [B, 32, 32]
    # 文本编码
    text_ids = tokenizer(texts)["input_ids"]
    # 拼接输入
    input_ids = torch.cat([text_ids, image_tokens.flatten(1)], dim=1)
    # 前向计算
    logits = transformer(text_ids, image_tokens)
    # 计算损失（仅图像部分）
    loss = nn.CrossEntropyLoss()(logits[:, -1024:].reshape(-1, 8192), 
                               image_tokens.flatten())
    # 反向传播
    loss.backward()
    optimizer.step()

```

# <font style="color:rgb(51, 51, 51);">Imagen（Google）</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：Imagen原理</font>

+ **<font style="color:rgb(51, 51, 51);">级联扩散模型</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">使用T5等大型语言模型编码文本。</font>
    - <font style="color:rgb(51, 51, 51);">通过多个扩散模型级联生成图像（低分辨率→高分辨率）。</font>
+ **<font style="color:rgb(51, 51, 51);">文本条件增强</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">文本嵌入被注入到扩散模型的每个分辨率阶段。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">文本编码</font>**<font style="color:rgb(51, 51, 51);">: c=T5_XXL(text)。</font>
2. **<font style="color:rgb(51, 51, 51);">基础扩散模型</font>**<font style="color:rgb(51, 51, 51);">: 生成64x64低分辨率图像。</font>
3. **<font style="color:rgb(51, 51, 51);">超分辨率模型</font>**<font style="color:rgb(51, 51, 51);">: 逐步生成256x256、1024x1024图像。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">文本编码能力强（T5-XXL）。</font>
    - <font style="color:rgb(51, 51, 51);">生成图像质量高。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">计算资源消耗极大。</font>
    - <font style="color:rgb(51, 51, 51);">未开源，仅限研究使用。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">专业设计、高精度视觉内容生成。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">知识蒸馏压缩模型大小。</font>
+ <font style="color:rgb(51, 51, 51);">优化级联模型的计算效率。</font>



# <font style="color:rgb(51, 51, 51);">MidJourney</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font>**<font style="color:rgb(51, 51, 51);">黑盒模型</font>**<font style="color:rgb(51, 51, 51);">:</font>

    - <font style="color:rgb(51, 51, 51);">推测基于扩散模型，结合艺术风格迁移技术。</font>
    - <font style="color:rgb(51, 51, 51);">用户反馈机制优化生成结果（社区驱动迭代）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">艺术风格突出，适合创意场景。</font>
    - <font style="color:rgb(51, 51, 51);">用户交互友好（Discord集成）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">可控性低，依赖提示词技巧。</font>
    - <font style="color:rgb(51, 51, 51);">未开源。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">数字艺术、插画、社交媒体内容。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ <font style="color:rgb(51, 51, 51);">增加局部编辑功能。</font>
+ <font style="color:rgb(51, 51, 51);">结合风格迁移模块。</font>



# <font style="color:rgb(51, 51, 51);">ControlNet</font>
# <font style="color:rgb(51, 51, 51);">Textual Inversion</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Textual Inversion 是一种针对文本到图像生成模型（如 Stable Diffusion）的轻量级微调技术，旨在通过少量示例图像将新概念嵌入模型的文本编码空间。该技术为个性化图像生成提供了高效的解决方案，后续可结合ControlNet等空间控制方法进一步提升生成可控性。最新进展如AnimateDiff已将其扩展到视频生成领域。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **核心思想**  
将新概念（如特定物体/风格）映射到预训练模型的文本嵌入空间，使用占位符token（如`<S*>`）表征新概念。
2. **实现机制**
    - **<font style="color:rgb(51, 51, 51);">文本编码器冻结</font>**<font style="color:rgb(51, 51, 51);">：保持CLIP文本编码器参数不变</font>
    - **<font style="color:rgb(51, 51, 51);">嵌入向量优化</font>**<font style="color:rgb(51, 51, 51);">：仅训练占位符token对应的嵌入向量</font>
    - **<font style="color:rgb(51, 51, 51);">扩散对齐</font>**<font style="color:rgb(51, 51, 51);">：通过重建损失使生成图像匹配示例图片</font>
3. **计算步骤**
    1. **数据准备**
        * <font style="color:rgb(51, 51, 51);">收集3-5张目标概念图像</font>
        * <font style="color:rgb(51, 51, 51);">构建提示模板（"A {概念} in {场景}"）</font>
    2. **模型初始化**
        * <font style="color:rgb(51, 51, 51);">添加新token到词汇表</font>
        * <font style="color:rgb(51, 51, 51);">初始化嵌入向量：随机值或预训练均值</font>
    3. **优化过程**
        * <font style="color:rgb(51, 51, 51);">前向传播：文本编码 → 扩散生成</font>
        * <font style="color:rgb(51, 51, 51);">损失计算：LPIPS + L2 混合损失</font>
        * <font style="color:rgb(51, 51, 51);">反向传播：仅更新新token的嵌入向量</font>
        * <font style="color:rgb(51, 51, 51);">迭代：通常500-3000步（1-2小时/GPU）</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

**<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">极低数据需求（3-5张图）</font>
2. <font style="color:rgb(51, 51, 51);">训练高效（仅优化1个嵌入向量）</font>
3. <font style="color:rgb(51, 51, 51);">保持模型原有生成能力</font>
4. <font style="color:rgb(51, 51, 51);">支持多概念组合</font>

**<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>

1. <font style="color:rgb(51, 51, 51);">生成多样性受限</font>
2. <font style="color:rgb(51, 51, 51);">视角一致性差</font>
3. <font style="color:rgb(51, 51, 51);">文本控制精度不足</font>
4. <font style="color:rgb(51, 51, 51);">难以捕捉复杂属性</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

| 场景 | 案例 | 效果 |
| --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">个性化生成</font> | <font style="color:rgb(51, 51, 51);">用户特定物品（如自家宠物）</font> | <font style="color:rgb(51, 51, 51);">⭐⭐⭐⭐</font> |
| <font style="color:rgb(51, 51, 51);">艺术风格迁移</font> | <font style="color:rgb(51, 51, 51);">特定画家风格复现</font> | <font style="color:rgb(51, 51, 51);">⭐⭐⭐</font> |
| <font style="color:rgb(51, 51, 51);">产品设计</font> | <font style="color:rgb(51, 51, 51);">品牌元素快速迭代</font> | <font style="color:rgb(51, 51, 51);">⭐⭐⭐⭐</font> |
| <font style="color:rgb(51, 51, 51);">文化遗产保护</font> | <font style="color:rgb(51, 51, 51);">古代器物数字化重建</font> | <font style="color:rgb(51, 51, 51);">⭐⭐</font> |


:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

1. **架构改进**
    - **<font style="color:rgb(51, 51, 51);">+LoRA</font>**<font style="color:rgb(51, 51, 51);">：在交叉注意力层添加低秩适配器</font>
    - **<font style="color:rgb(51, 51, 51);">Cones++</font>**<font style="color:rgb(51, 51, 51);">：引入对比学习增强语义区分度</font>
2. **训练优化**
    - <font style="color:rgb(51, 51, 51);">动态模板策略（随机组合提示词）</font>
    - <font style="color:rgb(51, 51, 51);">混合正则化损失（CLIP语义约束）</font>
3. **推理增强**
    - <font style="color:rgb(51, 51, 51);">注意力控制引导</font>
    - <font style="color:rgb(51, 51, 51);">多概念组合推理</font>

:::color5
**<font style="color:#601BDE;">5.性能对比</font>**

:::

| 方法 | 训练参数量 | VRAM消耗 | 训练时间 | 保真度 |
| --- | --- | --- | --- | --- |
| <font style="color:rgb(51, 51, 51);">Textual Inversion</font> | <font style="color:rgb(51, 51, 51);">~1KB</font> | <font style="color:rgb(51, 51, 51);">12GB</font> | <font style="color:rgb(51, 51, 51);">1h</font> | <font style="color:rgb(51, 51, 51);">中等</font> |
| <font style="color:rgb(51, 51, 51);">DreamBooth</font> | <font style="color:rgb(51, 51, 51);">3.5B</font> | <font style="color:rgb(51, 51, 51);">24GB</font> | <font style="color:rgb(51, 51, 51);">20min</font> | <font style="color:rgb(51, 51, 51);">高</font> |
| <font style="color:rgb(51, 51, 51);">LoRA</font> | <font style="color:rgb(51, 51, 51);">0.5M</font> | <font style="color:rgb(51, 51, 51);">16GB</font> | <font style="color:rgb(51, 51, 51);">30min</font> | <font style="color:rgb(51, 51, 51);">较高</font> |


:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
from diffusers import StableDiffusionPipeline
import torch

# 初始化模型
model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
tokenizer = model.tokenizer
text_encoder = model.text_encoder

# 添加新token
placeholder = "<S1>"
num_added = tokenizer.add_tokens(placeholder)
new_token_id = tokenizer.convert_tokens_to_ids(placeholder)

# 扩展嵌入层
with torch.no_grad():
    old_emb = text_encoder.get_input_embeddings().weight.data.mean(0)
    new_embeddings = torch.nn.Embedding(tokenizer.vocab_size + 1, 768)
    new_embeddings.weight.data[:-1] = text_encoder.get_input_embeddings().weight.data
    new_embeddings.weight.data[-1] = old_emb
    text_encoder.set_input_embeddings(new_embeddings)

# 训练配置
optimizer = torch.optim.AdamW([new_embeddings.weight[-1]], lr=5e-3)

# 训练循环
for batch in dataloader:
    optimizer.zero_grad()
    
    # 构建输入
    text = f"A {placeholder} cat"
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    
    # 获取嵌入
    embeddings = text_encoder.get_input_embeddings()(input_ids)
    
    # 扩散过程
    noise = torch.randn_like(images)
    timesteps = torch.randint(0, 1000, (1,))
    noisy_images = model.scheduler.add_noise(images, noise, timesteps)
    
    # 预测噪声
    noise_pred = model.unet(noisy_images, timesteps, encoder_hidden_states=embeddings).sample
    
    # 计算损失
    loss = torch.nn.functional.mse_loss(noise_pred, noise)
    loss.backward()
    optimizer.step()

```





# <font style="color:rgb(0, 0, 0);">SORA</font>
