# ⓵ Infra & 推理加速

<!-- source: yuque://zhongxian-iiot9/hlyypb/cdct1lkbbd7hhlun -->

# **英伟达**
**公司：****<font style="color:#117CEE;">英伟达</font>**

**岗位：****<font style="color:#117CEE;">大模型推理加速</font>**

**时间：****<font style="color:#117CEE;">24年</font>**

## 量化quantization部分
:::color5
1. **<font style="color:#601BDE;">说说你知道的那些针对LLM的量化技法？</font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743162729470-36a8895f-74db-42ed-b2f7-7d71be364d13.png)

:::

:::color5
2. **<font style="color:#601BDE;">smooth quant为什么可以解决int8 LLM的accuracy问题？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(25, 27, 31);">SmoothQuant （论文：</font>**<font style="color:rgb(25, 27, 31);">SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models</font>**<font style="color:rgb(25, 27, 31);">）是一种同时确保准确率且推理高效的训练后量化 (PTQ) 方法，可实现 8 比特权重、8 比特激活 (W8A8) 量化。由于权重很容易量化，而激活则较难量化，因此，SmoothQuant </font>**<font style="color:#ED740C;">引入平滑因子s来平滑激活异常值，通过数学上等效的变换将量化难度从激活转移到权重上。</font>**

<font style="color:rgb(13, 18, 57);">Smooth Quant之所以能有效解决INT8量化大型语言模型（LLM）的准确性问题，主要归因于其</font>**<font style="color:#74B602;">创新性地平衡了激活（activation）和权重（weight）的量化难度</font>**<font style="color:rgb(13, 18, 57);">，从而显著降低了量化误差</font>

:::

:::color5
3. **<font style="color:#601BDE;">bfloat16和fp16(half float point)同样内存大小，那么它们可以节约的内存大小应该是一样的吗？他们的优缺点主要有哪些？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(13, 18, 57);">bfloat16 和 FP16（半精度浮点数）在内存占用上确实相同（均为 16 位/2 字节），因此</font>**<font style="color:rgb(13, 18, 57);">两者节约的内存大小是相同的</font>**<font style="color:rgb(13, 18, 57);">（例如，相比 FP32 可减少 50% 的内存）。然而，它们在动态范围、精度、硬件支持和适用场景上存在显著差异。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743156236692-a72eef32-26bb-4ecc-a493-83c57141ab68.png)

:::

:::color5
4. **<font style="color:#601BDE;">量化怎么平衡精度和速度？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

**<font style="color:rgb(13, 18, 57);">核心原则</font>**<font style="color:rgb(13, 18, 57);">：通过量化层次、混合精度、QAT和硬件适配的组合策略，在精度损失可接受范围内最大化加速比。</font>

**<font style="color:rgb(13, 18, 57);">关键步骤</font>**<font style="color:rgb(13, 18, 57);">：校准数据筛选、层级别的保护、与硬件对齐的优化，并通过多次迭代调优最终方案。</font>

**<font style="color:rgb(13, 18, 57);">实验与调优流程</font>**

**<font style="color:rgb(13, 18, 57);">1.基准测试</font>**<font style="color:rgb(13, 18, 57);">：</font>

    - <font style="color:rgb(13, 18, 57);">记录原始模型的性能（精度、推理时间）。</font>

**<font style="color:rgb(13, 18, 57);">2.量化方案设计</font>**<font style="color:rgb(13, 18, 57);">：</font>

    - <font style="color:rgb(13, 18, 57);">根据模型结构选择量化层次（层粒度/通道粒度）。</font>
    - <font style="color:rgb(13, 18, 57);">排除关键层的量化（如最后一层全连接）。</font>

**<font style="color:rgb(13, 18, 57);">3.精度验证与迭代</font>**<font style="color:rgb(13, 18, 57);">：</font>

    - <font style="color:rgb(13, 18, 57);">使用验证集评估不同量化位数的精度损失。</font>
    - <font style="color:rgb(13, 18, 57);">使用校准数据调整缩放因子或激活函数。</font>

**<font style="color:rgb(13, 18, 57);">4.硬件级优化</font>**<font style="color:rgb(13, 18, 57);">：</font>

    - <font style="color:rgb(13, 18, 57);">部署到目标设备，观察实际加速比和精度下降。</font>
    - <font style="color:rgb(13, 18, 57);">调整校准策略或微调关键层的量化参数。</font>

**<font style="color:rgb(13, 18, 57);">5.自动化搜索</font>**<font style="color:rgb(13, 18, 57);">：</font>

    - <font style="color:rgb(13, 18, 57);">利用NAS（神经架构搜索）或量化算法（如AWS的Quantization Simplicity）自动寻找最优量化策略。</font>

**典型场景**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1743156397127-709f5aac-bda1-402f-9de7-cb54a2239247.png)

:::

## CUDA部分
:::color5
5. **<font style="color:#601BDE;">讲讲shared memory bank conflict的发生场景？以及你能想到哪些解决方案？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答</font>**

<font style="color:rgb(13, 18, 57);">共享内存的 Bank Conflict 是 GPU 编程中常见的性能问题，主要发生在同一 Warp 内的线程访问同一 Bank 的不同地址时，导致访问被串行化。</font>

**<font style="color:rgb(13, 18, 57);">发生场景</font>**

1. **<font style="color:rgb(13, 18, 57);">跨步访问（Strided Access）</font>**
    - <font style="color:rgb(13, 18, 57);">当线程按固定步长访问共享内存时（如二维数组按列访问），若步长与 Bank 数量（通常为32）成倍数关系，会导致多个线程访问同一 Bank。</font>
    - <font style="color:rgb(13, 18, 57);">例：一个</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">float</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">类型（4字节）的数组按列访问，若每行有32个元素，则相邻行的同一列元素会落在同一 Bank，引发 Bank Conflict。</font>
2. **<font style="color:rgb(13, 18, 57);">非对齐访问</font>**
    - <font style="color:rgb(13, 18, 57);">数据结构未对齐到 Bank 边界，导致线程访问跨多个 Bank，可能引发冲突（如结构体填充不当）。</font>
3. **<font style="color:rgb(13, 18, 57);">随机访问</font>**
    - <font style="color:rgb(13, 18, 57);">线程的随机内存访问模式可能导致不可预测的 Bank 冲突。</font>

**<font style="color:rgb(13, 18, 57);">解决方案</font>**

1. **<font style="color:rgb(13, 18, 57);">调整数据布局（Padding）</font>**
    - **<font style="color:rgb(13, 18, 57);">原理</font>**<font style="color:rgb(13, 18, 57);">：在数据行末尾添加冗余元素，打破跨步访问的冲突。</font>
    - **<font style="color:rgb(13, 18, 57);">示例</font>**<font style="color:rgb(13, 18, 57);">：将共享内存数组从</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">[N][32]</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">调整为</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">[N][33]</font>`<font style="color:rgb(13, 18, 57);">，避免列访问时 Bank 对齐。</font>
    - **<font style="color:rgb(13, 18, 57);">适用场景</font>**<font style="color:rgb(13, 18, 57);">：矩阵转置、跨步数据访问。</font>
2. **<font style="color:rgb(13, 18, 57);">优化访问模式</font>**
    - **<font style="color:rgb(13, 18, 57);">合并访问</font>**<font style="color:rgb(13, 18, 57);">：让同一 Warp 的线程访问连续内存地址，利用 Bank 的广播机制。</font>
    - **<font style="color:rgb(13, 18, 57);">示例</font>**<font style="color:rgb(13, 18, 57);">：矩阵乘法中，按行读取全局内存后，按列写入共享内存时使用 Padding 避免冲突。</font>
3. **<font style="color:rgb(13, 18, 57);">利用 Bank 广播</font>**
    - **<font style="color:rgb(13, 18, 57);">原理</font>**<font style="color:rgb(13, 18, 57);">：同一 Warp 内所有线程读取同一 Bank 的同一地址时，触发广播机制，无冲突。</font>
    - **<font style="color:rgb(13, 18, 57);">适用场景</font>**<font style="color:rgb(13, 18, 57);">：读取常量或共享数据（如卷积核）。</font>
4. **<font style="color:rgb(13, 18, 57);">调整线程块配置</font>**
    - **<font style="color:rgb(13, 18, 57);">块大小</font>**<font style="color:rgb(13, 18, 57);">：使用与 Bank 数量互质的线程块大小（如31或33），减少跨步冲突概率。</font>
5. **<font style="color:rgb(13, 18, 57);">数据分块与重组</font>**
    - **<font style="color:rgb(13, 18, 57);">原理</font>**<font style="color:rgb(13, 18, 57);">：将数据划分为小块，重新排列存储顺序（如 Z-order 曲线）。</font>
    - **<font style="color:rgb(13, 18, 57);">适用场景</font>**<font style="color:rgb(13, 18, 57);">：图像处理、高维数据访问。</font>
6. **<font style="color:rgb(13, 18, 57);">使用向量化访问</font>**
    - **<font style="color:rgb(13, 18, 57);">原理</font>**<font style="color:rgb(13, 18, 57);">：通过 </font>`<font style="color:rgb(13, 18, 57);">float4</font>`<font style="color:rgb(13, 18, 57);"> 等向量类型一次性读取多个数据，减少访问次数。</font>
    - **<font style="color:rgb(13, 18, 57);">示例</font>**<font style="color:rgb(13, 18, 57);">：在矩阵乘法中，使用 </font>`<font style="color:rgb(13, 18, 57);">float4</font>`<font style="color:rgb(13, 18, 57);"> 读取全局内存，提升内存吞吐量。</font>

:::

:::color5
7. **<font style="color:#601BDE;">CUDA里面如何分配GPU显存？为什么里面的参数是二级指针？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(13, 18, 57);">在CUDA中分配GPU显存主要通过</font>`<font style="color:rgb(13, 18, 57);">cudaMalloc</font>`<font style="color:rgb(13, 18, 57);">函数实现，其参数使用二级指针的原因如下：</font>

:::

**<font style="color:rgb(13, 18, 57);">如何分配GPU显存？</font>**

1. **<font style="color:rgb(13, 18, 57);">声明设备指针</font>**<font style="color:rgb(13, 18, 57);">：首先定义一个指向设备内存的指针变量，例如</font>`<font style="color:rgb(13, 18, 57);">int *d_array;</font>`<font style="color:rgb(13, 18, 57);">。</font>
2. **<font style="color:rgb(13, 18, 57);">调用cudaMalloc</font>**<font style="color:rgb(13, 18, 57);">：使用</font>`<font style="color:rgb(13, 18, 57);">cudaMalloc</font>`<font style="color:rgb(13, 18, 57);">分配显存，传递指针变量的地址和所需大小：</font>

```c
cudaError_t err = cudaMalloc((void**)&d_array, 100 * sizeof(int));
```

3. **<font style="color:rgb(13, 18, 57);">错误检查</font>**<font style="color:rgb(13, 18, 57);">：检查返回值以确保分配成功：</font>

```c
if (err != cudaSuccess) {
    // 处理错误（如内存不足）
}
```

4. **<font style="color:rgb(13, 18, 57);">释放显存</font>**<font style="color:rgb(13, 18, 57);">：使用完毕后，通过</font>`<font style="color:rgb(13, 18, 57);">cudaFree</font>`<font style="color:rgb(13, 18, 57);">释放显存：</font>

```c
cudaFree(d_array);
```

**<font style="color:rgb(13, 18, 57);">为什么参数是二级指针？</font>**

+ **<font style="color:rgb(13, 18, 57);">按值传递的限制</font>**<font style="color:rgb(13, 18, 57);">：C语言中函数参数是值传递的。若直接传递一级指针（如</font>`<font style="color:rgb(13, 18, 57);">void* ptr</font>`<font style="color:rgb(13, 18, 57);">），函数内部修改</font>`<font style="color:rgb(13, 18, 57);">ptr</font>`<font style="color:rgb(13, 18, 57);">仅会影响副本，无法修改外部的指针变量。</font>
+ **<font style="color:rgb(13, 18, 57);">修改指针的需求</font>**<font style="color:rgb(13, 18, 57);">：</font>`<font style="color:rgb(13, 18, 57);">cudaMalloc</font>`<font style="color:rgb(13, 18, 57);">需将分配的显存地址写入调用者的指针变量。为此，必须传递指针的地址（即二级指针</font>`<font style="color:rgb(13, 18, 57);">void**</font>`<font style="color:rgb(13, 18, 57);">），使函数能通过解引用修改原始指针的值。</font>
+ **<font style="color:rgb(13, 18, 57);">类比C语言中的malloc</font>**<font style="color:rgb(13, 18, 57);">：类似以下代码：</font>

```c
void allocate(int** ptr) {
    *ptr = malloc(sizeof(int) * 10);
}
// 调用时传递指针的地址
int *arr;
allocate(&arr);
```

`<font style="color:rgb(13, 18, 57);">cudaMalloc</font>`<font style="color:rgb(13, 18, 57);">采用相同机制，确保外部指针正确指向显存。</font>

:::color5
8. **<font style="color:#601BDE;">优化CUDA程序的访存效率，你可以想到哪些？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

<font style="color:rgb(13, 18, 57);">1. 全局内存优化</font>

+ **<font style="color:rgb(13, 18, 57);">合并访问（Coalesced Access）</font>**
    - <font style="color:rgb(13, 18, 57);">确保相邻线程访问连续的全局内存地址（如</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">threadIdx.x</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">对应数据的连续地址），合并为单个内存事务。</font>
    - **<font style="color:rgb(13, 18, 57);">示例</font>**<font style="color:rgb(13, 18, 57);">：矩阵转置时，使用共享内存中转以避免交叉访问。</font>
+ **<font style="color:rgb(13, 18, 57);">对齐访问</font>**
    - <font style="color:rgb(13, 18, 57);">使用</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">cudaMallocPitch</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">分配二维内存，保证行对齐（如128字节）。</font>
    - <font style="color:rgb(13, 18, 57);">结构体通过</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">__align__</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">指令对齐。</font>
+ **<font style="color:rgb(13, 18, 57);">向量化加载（Vectorized Load）</font>**
    - <font style="color:rgb(13, 18, 57);">使用</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">float4</font>`<font style="color:rgb(13, 18, 57);">、</font>`<font style="color:rgb(13, 18, 57);">int2</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">等宽类型指令，提升内存吞吐量。</font>

```cpp
float4 data = reinterpret_cast<float4*>(global_ptr)[tid];
```

+ **<font style="color:rgb(13, 18, 57);">内存布局优化</font>**
    - **<font style="color:rgb(13, 18, 57);">数组结构体（SoA）</font>**<font style="color:rgb(13, 18, 57);">：将同类型数据连续存储（如</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">float *x, *y, *z</font>`<font style="color:rgb(13, 18, 57);">），优于结构体数组（AoS）。</font>
    - **<font style="color:rgb(13, 18, 57);">示例</font>**<font style="color:rgb(13, 18, 57);">：粒子系统中，将位置、速度分离存储。</font>



<font style="color:rgb(13, 18, 57);">2. 共享内存优化</font>

+ **<font style="color:rgb(13, 18, 57);">Bank冲突避免</font>**
    - <font style="color:rgb(13, 18, 57);">确保同一线程束内的线程访问不同bank（32 banks，4字节步长）。</font>
    - **<font style="color:rgb(13, 18, 57);">方法</font>**<font style="color:rgb(13, 18, 57);">：填充共享内存（如</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">__shared__ float data[32][33]</font>`<font style="color:rgb(13, 18, 57);">）或调整访问步长。</font>
+ **<font style="color:rgb(13, 18, 57);">数据复用</font>**
    - <font style="color:rgb(13, 18, 57);">将频繁访问的全局数据缓存在共享内存中，如矩阵乘法中的分块加载。</font>

```cpp
__shared__ float tile[TILE_SIZE][TILE_SIZE];
tile[threadIdx.y][threadIdx.x] = global_data[global_index];
__syncthreads();
```

<font style="color:rgb(13, 18, 57);">3. 常量内存与纹理内存</font>

+ **<font style="color:rgb(13, 18, 57);">常量内存</font>**
    - <font style="color:rgb(13, 18, 57);">使用</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">__constant__</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">存储只读数据（如参数表），利用缓存加速访问。</font>
+ **<font style="color:rgb(13, 18, 57);">纹理内存</font>**
    - <font style="color:rgb(13, 18, 57);">对空间局部性强的数据（如图像处理），利用纹理缓存和硬件插值。</font>

<font style="color:rgb(13, 18, 57);">4. 寄存器优化</font>

+ **<font style="color:rgb(13, 18, 57);">减少寄存器溢出</font>**
    - <font style="color:rgb(13, 18, 57);">限制局部变量数量，避免使用过多导致数据溢出到本地内存。</font>
    - <font style="color:rgb(13, 18, 57);">通过</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">__launch_bounds__</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">调整寄存器使用和线程块大小的平衡。</font>

:::color5
9. **<font style="color:#601BDE;">优化CUDA程序的计算效率，你又可以想到哪些？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(13, 18, 57);">1. 提高并行粒度</font>

+ **<font style="color:rgb(13, 18, 57);">合理选择线程块和网格大小</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">线程块的大小（</font>`<font style="color:rgb(13, 18, 57);">blockDim.x/y/z</font>`<font style="color:rgb(13, 18, 57);">）应与SM（流多处理器）的硬件资源（如寄存器、共享内存）匹配，以充分利用硬件并行性。例如，大多数GPU的SM支持最多1024个线程（如Ampere架构）。</font>
    - <font style="color:rgb(13, 18, 57);">线程块的大小应是</font>**<font style="color:rgb(13, 18, 57);">块尺寸的倍数</font>**<font style="color:rgb(13, 18, 57);">（如32、64、128、256等），以确保Warp（32线程）的完整性和合并内存访问。</font>
    - <font style="color:rgb(13, 18, 57);">网格（grid）的大小应足够大，以覆盖所有SM，避免计算资源浪费。</font>
+ **<font style="color:rgb(13, 18, 57);">平衡计算与访存比例</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">对于计算密集型代码（如矩阵乘法），应选择较大的线程块以减少线程开销。</font>
    - <font style="color:rgb(13, 18, 57);">对于内存密集型代码（如数据传输），需平衡线程块大小与共享内存的使用，避免因内存带宽不足导致的性能瓶颈。</font>

<font style="color:rgb(13, 18, 57);">2. 优化内存访问模式</font>

<font style="color:rgb(13, 18, 57);">（1）全局内存优化</font>

+ **<font style="color:rgb(13, 18, 57);">合并内存访问（Coalesced Access）</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">确保同一warp内的线程访问连续的全局内存地址。例如，线程</font>`<font style="color:rgb(13, 18, 57);">tid</font>`<font style="color:rgb(13, 18, 57);">访问</font>`<font style="color:rgb(13, 18, 57);">array[tid]</font>`<font style="color:rgb(13, 18, 57);">比</font>`<font style="color:rgb(13, 18, 57);">array[tid * stride]</font>`<font style="color:rgb(13, 18, 57);">更高效。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">__align__</font>`<font style="color:rgb(13, 18, 57);">和</font>`<font style="color:rgb(13, 18, 57);">__align__(16)</font>`<font style="color:rgb(13, 18, 57);">等关键字对数据结构进行对齐，确保内存访问对齐到16/32/64字节边界。</font>
+ **<font style="color:rgb(13, 18, 57);">减少全局内存访问次数</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">将频繁访问的数据加载到**共享内存（Shared Memory）**中，减少对全局内存的访问。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>**<font style="color:rgb(13, 18, 57);">循环展开</font>**<font style="color:rgb(13, 18, 57);">或</font>**<font style="color:rgb(13, 18, 57);">数据复用</font>**<font style="color:rgb(13, 18, 57);">技术，减少重复访问全局内存。</font>

<font style="color:rgb(13, 18, 57);">（2）共享内存优化</font>

+ **<font style="color:rgb(13, 18, 57);">缓存数据</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">将需要频繁访问的全局内存数据（如小矩阵或邻域数据）加载到共享内存中，减少全局内存带宽压力。</font>
    - <font style="color:rgb(13, 18, 57);">确保共享内存的访问模式是合并的，避免冲突（如同一bank的冲突）。</font>
+ **<font style="color:rgb(13, 18, 57);">减少线程同步开销</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">__syncthreads()</font>`<font style="color:rgb(13, 18, 57);">时，确保所有线程都到达同步点，避免死锁或数据竞争。</font>
    - <font style="color:rgb(13, 18, 57);">避免在循环内部频繁同步，尽量将同步操作放在循环外。</font>

#### **<font style="color:rgb(13, 18, 57);">（3）常量内存（Constant Memory）和纹理内存（Texture Memory）</font>**
+ **<font style="color:rgb(13, 18, 57);">常量内存</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">对于只读且共享的常量数据，使用</font>`<font style="color:rgb(13, 18, 57);">__constant__</font>`<font style="color:rgb(13, 18, 57);">关键字存储，利用GPU的常量缓存。</font>
    - <font style="color:rgb(13, 18, 57);">数据需对齐到4字节边界，并尽可能使用</font>`<font style="color:rgb(13, 18, 57);">__ldg()</font>`<font style="color:rgb(13, 18, 57);">指令（针对L1缓存优化）。</font>
+ **<font style="color:rgb(13, 18, 57);">纹理内存</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">利用纹理缓存的压缩和空间局部性优化，适合访问具有空间局部性的数据（如图像）。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">cudaBindTexture()</font>`<font style="color:rgb(13, 18, 57);">绑定纹理，通过</font>`<font style="color:rgb(13, 18, 57);">tex2D()</font>`<font style="color:rgb(13, 18, 57);">等函数访问。</font>



<font style="color:rgb(13, 18, 57);">3. 减少计算冗余</font>

+ **<font style="color:rgb(13, 18, 57);">消除分支发散（Branch Divergence）</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">避免同一warp内的线程执行不同分支，否则会导致其他线程闲置。例如，将条件判断移到循环外部。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">__unroll</font>`<font style="color:rgb(13, 18, 57);">或</font>`<font style="color:rgb(13, 18, 57);">#pragma unroll</font>`<font style="color:rgb(13, 18, 57);">指令展开循环，减少分支判断。</font>
+ **<font style="color:rgb(13, 18, 57);">数学函数优化</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">使用内联汇编或CUDA内置函数（如</font>`<font style="color:rgb(13, 18, 57);">__fma_rn()</font>`<font style="color:rgb(13, 18, 57);">）代替复杂的数学运算。</font>
    - <font style="color:rgb(13, 18, 57);">对于精度要求不高的场景，使用</font>`<font style="color:rgb(13, 18, 57);">--use_fast_math</font>`<font style="color:rgb(13, 18, 57);">编译标志加速数学计算。</font>
+ **<font style="color:rgb(13, 18, 57);">减少寄存器压力</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">避免在核函数中使用过多局部变量，减少寄存器溢出导致的spill（溢出到内存）。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">-Xptxas -v</font>`<font style="color:rgb(13, 18, 57);">查看寄存器使用情况，或通过</font>`<font style="color:rgb(13, 18, 57);">-maxrregcount</font>`<font style="color:rgb(13, 18, 57);">限制寄存器数量。</font>

<font style="color:rgb(13, 18, 57);">4. 利用硬件特性</font>

+ **<font style="color:rgb(13, 18, 57);">L1/L2缓存优化</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">对于小块数据，利用L1缓存的高速缓存特性（如矩阵乘法中的tile划分）。</font>
    - <font style="color:rgb(13, 18, 57);">使用</font>`<font style="color:rgb(13, 18, 57);">cudaFuncSetCacheConfig()</font>`<font style="color:rgb(13, 18, 57);">设置缓存配置（</font>`<font style="color:rgb(13, 18, 57);">cudaFuncCachePreferL1</font>`<font style="color:rgb(13, 18, 57);">或</font>`<font style="color:rgb(13, 18, 57);">cudaFuncCachePreferShared</font>`<font style="color:rgb(13, 18, 57);">）。</font>
+ **<font style="color:rgb(13, 18, 57);">统一内存（Unified Memory）</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">在多GPU系统中，使用统一内存简化数据管理，但需注意跨GPU访问的性能开销（需通过</font>`<font style="color:rgb(13, 18, 57);">cudaMemAdvise()</font>`<font style="color:rgb(13, 18, 57);">显式控制数据放置）。</font>
+ **<font style="color:rgb(13, 18, 57);">显式使用多处理器（Multi-Processor, SM）资源</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">对于计算密集型任务，确保每个SM的线程块数量足够多，以隐藏延迟（如内存访问或分支延迟）。</font>

:::



## 大模型部分
:::color5
10. **<font style="color:#601BDE;">有哪些encoder-only、decoder-only、encoder-decoder的模型？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

| **架构** | **典型任务** | **训练目标** | **代表模型** |
| --- | --- | --- | --- |
| <font style="color:rgb(13, 18, 57);">Encoder-Only</font> | <font style="color:rgb(13, 18, 57);">理解/分类</font> | <font style="color:rgb(13, 18, 57);">MLM、NSP</font> | <font style="color:rgb(13, 18, 57);">BERT、RoBERTa</font> |
| <font style="color:rgb(13, 18, 57);">Decoder-Only</font> | <font style="color:rgb(13, 18, 57);">生成</font> | <font style="color:rgb(13, 18, 57);">自回归语言模型</font> | <font style="color:rgb(13, 18, 57);">GPT、PaLM、主流LLM</font> |
| <font style="color:rgb(13, 18, 57);">Encoder-Decoder</font> | <font style="color:rgb(13, 18, 57);">Seq2Seq</font> | <font style="color:rgb(13, 18, 57);">跨模态损失（如交叉熵）</font> | <font style="color:rgb(13, 18, 57);">T5、BART</font> |


:::color5
11. **<font style="color:#601BDE;">随着seqlen的增加，你觉得encoder-only的模型和decoder-only的模型的计算量和访存量会是哪些变化趋势？为什么？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

**<font style="color:rgb(13, 18, 57);">1. 计算量（FLOPs）的变化趋势</font>**

<font style="color:rgb(13, 18, 57);">(1) Encoder-only模型（如BERT）</font>

+ **<font style="color:rgb(13, 18, 57);">自注意力层</font>**<font style="color:rgb(13, 18, 57);">：计算复杂度为</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen² × d)</font>**<font style="color:rgb(13, 18, 57);">，其中</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">d</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">是模型维度。随着</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">增加，计算量呈</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">平方级增长</font>**<font style="color:rgb(13, 18, 57);">。</font>
+ **<font style="color:rgb(13, 18, 57);">前馈网络（FFN）</font>**<font style="color:rgb(13, 18, 57);">：计算复杂度为</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen × d²)</font>**<font style="color:rgb(13, 18, 57);">，随</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">线性增长。</font>
+ **<font style="color:rgb(13, 18, 57);">总体趋势</font>**<font style="color:rgb(13, 18, 57);">：当</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">较大时，自注意力层的平方项占主导，整体计算量主要受</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen² × d)</font>**<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">驱动。</font>

<font style="color:rgb(13, 18, 57);">(2) Decoder-only模型（如GPT）</font>

+ **<font style="color:rgb(13, 18, 57);">自注意力层</font>**<font style="color:rgb(13, 18, 57);">：同样需要计算因果掩码的自注意力，复杂度仍为</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen² × d)</font>**<font style="color:rgb(13, 18, 57);">，平方级增长。</font>
+ **<font style="color:rgb(13, 18, 57);">前馈网络</font>**<font style="color:rgb(13, 18, 57);">：与Encoder相同，复杂度为</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen × d²)</font>**<font style="color:rgb(13, 18, 57);">。</font>
+ **<font style="color:rgb(13, 18, 57);">总体趋势</font>**<font style="color:rgb(13, 18, 57);">：与Encoder类似，计算量主要由自注意力层的平方项主导。</font>

<font style="color:rgb(13, 18, 57);">对比</font>

+ **<font style="color:rgb(13, 18, 57);">相同点</font>**<font style="color:rgb(13, 18, 57);">：两种模型的计算量均受自注意力层的</font><font style="color:rgb(13, 18, 57);"> </font>**<font style="color:rgb(13, 18, 57);">O(seqlen² × d)</font>**<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">主导，随</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">呈平方增长。</font>
+ **<font style="color:rgb(13, 18, 57);">差异点</font>**<font style="color:rgb(13, 18, 57);">：Decoder的因果掩码可能略微降低实际计算量（部分位置无需计算），但复杂度阶数不变。</font>

**<font style="color:rgb(13, 18, 57);">2. 访存量（Memory Access）的变化趋势</font>**

<font style="color:rgb(13, 18, 57);">访存量主要取决于中间激活（如注意力矩阵）和参数缓存的规模。</font>

<font style="color:rgb(13, 18, 57);">(1) Encoder-only模型</font>

+ **<font style="color:rgb(13, 18, 57);">中间激活</font>**<font style="color:rgb(13, 18, 57);">：存储注意力矩阵（大小为</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen²</font>`<font style="color:rgb(13, 18, 57);">），访存量随</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen²</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">增长。</font>
+ **<font style="color:rgb(13, 18, 57);">参数缓存</font>**<font style="color:rgb(13, 18, 57);">：模型参数固定，访存量与</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">无关。</font>

<font style="color:rgb(13, 18, 57);">(2) Decoder-only模型</font>

+ **<font style="color:rgb(13, 18, 57);">中间激活</font>**<font style="color:rgb(13, 18, 57);">：与Encoder类似，需存储因果掩码后的注意力矩阵（大小仍为</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen²</font>`<font style="color:rgb(13, 18, 57);">），访存量同样呈平方级增长。</font>
+ **<font style="color:rgb(13, 18, 57);">KV缓存（推理阶段）</font>**<font style="color:rgb(13, 18, 57);">：在生成式推理中需缓存历史Key/Value，访存量随</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">线性增长（O(seqlen × d)），但此特性仅限于推理阶段。</font>

<font style="color:rgb(13, 18, 57);">对比</font>

+ **<font style="color:rgb(13, 18, 57);">训练阶段</font>**<font style="color:rgb(13, 18, 57);">：两者访存量均随</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">seqlen²</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">增长，因需存储注意力矩阵。</font>
+ **<font style="color:rgb(13, 18, 57);">推理阶段</font>**<font style="color:rgb(13, 18, 57);">：Decoder的KV缓存引入线性访存量增长，但Encoder无此特性。</font>

:::

:::color5
12. **<font style="color:#601BDE;">说说你知道的大模型训练or推理的常用优化手段 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(13, 18, 57);">在大模型训练和推理中，优化手段多种多样，核心目标是提升效率、降低资源消耗。</font>

<font style="color:rgb(13, 18, 57);">一、训练阶段优化</font>

1. **<font style="color:rgb(13, 18, 57);">并行策略</font>**
    - **<font style="color:rgb(13, 18, 57);">数据并行</font>**<font style="color:rgb(13, 18, 57);">：将数据分片到多设备，同步梯度（如PyTorch DDP）。</font>
    - **<font style="color:rgb(13, 18, 57);">模型并行</font>**<font style="color:rgb(13, 18, 57);">：拆分模型层到不同设备（如Megatron-LM的</font>**<font style="color:rgb(13, 18, 57);">张量并行</font>**<font style="color:rgb(13, 18, 57);">）。</font>
    - **<font style="color:rgb(13, 18, 57);">流水线并行</font>**<font style="color:rgb(13, 18, 57);">：将模型按层分段，多设备级联（如PipeTransformer）。</font>
    - **<font style="color:rgb(13, 18, 57);">混合并行</font>**<font style="color:rgb(13, 18, 57);">：结合上述策略，如3D并行（DeepSpeed + Megatron-LM）。</font>
2. **<font style="color:rgb(13, 18, 57);">内存优化</font>**
    - **<font style="color:rgb(13, 18, 57);">混合精度训练（AMP）</font>**<font style="color:rgb(13, 18, 57);">：FP16计算+FP32主权重，节省显存并加速。</font>
    - **<font style="color:rgb(13, 18, 57);">ZeRO优化</font>**<font style="color:rgb(13, 18, 57);">（DeepSpeed）：分阶段优化内存，Stage-3可消除模型状态冗余。</font>
    - **<font style="color:rgb(13, 18, 57);">梯度检查点（Gradient Checkpointing）</font>**<font style="color:rgb(13, 18, 57);">：牺牲计算时间换内存，反向传播时重算中间激活值。</font>
    - **<font style="color:rgb(13, 18, 57);">激活卸载（Activation Offloading）</font>**<font style="color:rgb(13, 18, 57);">：将激活值临时存到CPU内存，减少GPU占用。</font>
3. **<font style="color:rgb(13, 18, 57);">优化器与参数调整</font>**
    - **<font style="color:rgb(13, 18, 57);">AdamW/LAMB优化器</font>**<font style="color:rgb(13, 18, 57);">：自适应学习率，避免权重衰减干扰参数更新。</font>
    - **<font style="color:rgb(13, 18, 57);">学习率预热（Warmup）</font>**<font style="color:rgb(13, 18, 57);">：初始阶段逐步增加学习率，防止梯度爆炸。</font>
    - **<font style="color:rgb(13, 18, 57);">动态批处理（Dynamic Batching）</font>**<font style="color:rgb(13, 18, 57);">：自动调整批大小，平衡内存与吞吐。</font>
4. **<font style="color:rgb(13, 18, 57);">其他技术</font>**
    - **<font style="color:rgb(13, 18, 57);">Flash Attention</font>**<font style="color:rgb(13, 18, 57);">：优化注意力计算，减少显存访问和计算复杂度。</font>
    - **<font style="color:rgb(13, 18, 57);">MOE架构</font>**<font style="color:rgb(13, 18, 57);">（混合专家模型）：如Switch Transformer，稀疏激活降低计算量。</font>
    - **<font style="color:rgb(13, 18, 57);">参数高效微调</font>**<font style="color:rgb(13, 18, 57);">：LoRA、Adapter等仅微调部分参数，减少训练成本。</font>



<font style="color:rgb(13, 18, 57);">二、推理阶段优化</font>

1. **<font style="color:rgb(13, 18, 57);">模型压缩</font>**
    - **<font style="color:rgb(13, 18, 57);">量化（Quantization）</font>**<font style="color:rgb(13, 18, 57);">：将FP32转为INT8/FP16（如TensorRT、GGML）。</font>
    - **<font style="color:rgb(13, 18, 57);">剪枝（Pruning）</font>**<font style="color:rgb(13, 18, 57);">：移除冗余权重（如非结构化/结构化剪枝）。</font>
    - **<font style="color:rgb(13, 18, 57);">知识蒸馏（Knowledge Distillation）</font>**<font style="color:rgb(13, 18, 57);">：用大模型训练轻量级学生模型。</font>
2. **<font style="color:rgb(13, 18, 57);">计算加速</font>**
    - **<font style="color:rgb(13, 18, 57);">算子融合（Kernel Fusion）</font>**<font style="color:rgb(13, 18, 57);">：合并多个操作为单一内核，减少显存访问（如TensorRT）。</font>
    - **<font style="color:rgb(13, 18, 57);">KV Cache缓存</font>**<font style="color:rgb(13, 18, 57);">：生成任务中缓存注意力键值，避免重复计算。</font>
    - **<font style="color:rgb(13, 18, 57);">推测解码（Speculative Decoding）</font>**<font style="color:rgb(13, 18, 57);">：用小模型预测结果，大模型快速验证。</font>
3. **<font style="color:rgb(13, 18, 57);">系统级优化</font>**
    - **<font style="color:rgb(13, 18, 57);">动态批处理</font>**<font style="color:rgb(13, 18, 57);">：合并不同长度输入，提升吞吐（如HuggingFace TGI）。</font>
    - **<font style="color:rgb(13, 18, 57);">显存管理</font>**<font style="color:rgb(13, 18, 57);">：如vLLM的</font>**<font style="color:rgb(13, 18, 57);">Paged Attention</font>**<font style="color:rgb(13, 18, 57);">，优化KV Cache显存分配。</font>
    - **<font style="color:rgb(13, 18, 57);">硬件适配</font>**<font style="color:rgb(13, 18, 57);">：利用TPU/NPU等专用加速器，或CUDA Graph减少启动开销。</font>
4. **<font style="color:rgb(13, 18, 57);">框架支持</font>**
    - **<font style="color:rgb(13, 18, 57);">推理框架</font>**<font style="color:rgb(13, 18, 57);">：ONNX Runtime、TensorRT、Triton Inference Server。</font>
    - **<font style="color:rgb(13, 18, 57);">服务优化</font>**<font style="color:rgb(13, 18, 57);">：模型分片、请求批处理、异步推理（如NVIDIA Triton）。</font>



<font style="color:rgb(13, 18, 57);">三、工具与库</font>

+ **<font style="color:rgb(13, 18, 57);">训练框架</font>**<font style="color:rgb(13, 18, 57);">：DeepSpeed（ZeRO优化）、Megatron-LM（并行策略）、HuggingFace Accelerate。</font>
+ **<font style="color:rgb(13, 18, 57);">推理框架</font>**<font style="color:rgb(13, 18, 57);">：vLLM（高吞吐）、TensorRT-LLM（NVIDIA优化）、OpenVINO（Intel CPU支持）。</font>
+ **<font style="color:rgb(13, 18, 57);">硬件支持</font>**<font style="color:rgb(13, 18, 57);">：NVIDIA GPU（CUDA/TensorCore）、Google TPU、华为昇腾NPU。</font>



<font style="color:rgb(13, 18, 57);">四、选择策略</font>

+ **<font style="color:rgb(13, 18, 57);">训练侧</font>**<font style="color:rgb(13, 18, 57);">：优先考虑并行策略和内存优化（如ZeRO-3 + 流水线并行）。</font>
+ **<font style="color:rgb(13, 18, 57);">推理侧</font>**<font style="color:rgb(13, 18, 57);">：量化+算子融合+动态批处理组合可显著降低延迟。</font>
+ **<font style="color:rgb(13, 18, 57);">资源受限场景</font>**<font style="color:rgb(13, 18, 57);">：小模型蒸馏+低精度量化（如手机端部署）。</font>

:::

:::color5
13. **<font style="color:#601BDE;">一般会对哪些大模型里面的算子做算子融合，说说你知道的 </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(13, 18, 57);">在大模型训练和推理中，算子融合（Operator Fusion）是优化计算效率的关键技术，主要目的是减少内存访问开销和内核启动次数，同时提高计算密度。</font>

<font style="color:rgb(13, 18, 57);">1. Transformer 架构中的融合</font>

+ **<font style="color:rgb(13, 18, 57);">矩阵乘法 + Softmax + Masking + Dropout</font>**
    - **<font style="color:rgb(13, 18, 57);">场景</font>**<font style="color:rgb(13, 18, 57);">：自注意力机制中的</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">QK^T</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">矩阵乘法后接 Softmax、掩码（如因果掩码）和 Dropout。</font>
    - **<font style="color:rgb(13, 18, 57);">融合原因</font>**<font style="color:rgb(13, 18, 57);">：避免中间结果（如</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">QK^T</font>`<font style="color:rgb(13, 18, 57);">）写回全局内存，直接在一个内核中完成计算，减少显存带宽压力。</font>
    - **<font style="color:rgb(13, 18, 57);">典型优化</font>**<font style="color:rgb(13, 18, 57);">：NVIDIA 的</font><font style="color:rgb(13, 18, 57);"> </font>[FlashAttention](https://arxiv.org/abs/2205.14135)<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">将矩阵乘、Softmax 和掩码融合，显著降低显存占用。</font>
+ **<font style="color:rgb(13, 18, 57);">Add + LayerNorm</font>**
    - **<font style="color:rgb(13, 18, 57);">场景</font>**<font style="color:rgb(13, 18, 57);">：残差连接后的 LayerNorm（如 Transformer 中的</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">x = LayerNorm(x + Sublayer(x))</font>`<font style="color:rgb(13, 18, 57);">）。</font>
    - **<font style="color:rgb(13, 18, 57);">融合原因</font>**<font style="color:rgb(13, 18, 57);">：将加法与归一化合并，减少对显存的多次读写。</font>



<font style="color:rgb(13, 18, 57);">2. 激活函数与线性层的融合</font>

+ **<font style="color:rgb(13, 18, 57);">Linear/Conv + ReLU/GELU/SiLU</font>**
    - **<font style="color:rgb(13, 18, 57);">场景</font>**<font style="color:rgb(13, 18, 57);">：全连接层或卷积层后接激活函数（如 BERT 中的</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">GELU(Linear(x))</font>`<font style="color:rgb(13, 18, 57);">）。</font>
    - **<font style="color:rgb(13, 18, 57);">融合原因</font>**<font style="color:rgb(13, 18, 57);">：合并乘加运算（GEMM）与激活函数的逐元素计算，避免中间结果保存。</font>
    - **<font style="color:rgb(13, 18, 57);">硬件支持</font>**<font style="color:rgb(13, 18, 57);">：CUDA 的</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">cublasLtMatMul</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">支持融合偏置（Bias）和激活函数。</font>



<font style="color:rgb(13, 18, 57);">3. 归一化层的融合</font>

+ **<font style="color:rgb(13, 18, 57);">Conv + BatchNorm</font>**
    - **<font style="color:rgb(13, 18, 57);">场景</font>**<font style="color:rgb(13, 18, 57);">：卷积层后接批量归一化（推理阶段）。</font>
    - **<font style="color:rgb(13, 18, 57);">融合原因</font>**<font style="color:rgb(13, 18, 57);">：在推理时，BatchNorm 的均值和方差固定，可合并到卷积的权重中，减少计算量。</font>
    - **<font style="color:rgb(13, 18, 57);">公式</font>**<font style="color:rgb(13, 18, 57);">：将 BatchNorm 的缩放（γ）和偏移（β）融合到卷积核参数中。</font>



<font style="color:rgb(13, 18, 57);">4. 混合精度训练中的融合</font>

+ **<font style="color:rgb(13, 18, 57);">FP16 Cast + All-Reduce</font>**
    - **<font style="color:rgb(13, 18, 57);">场景</font>**<font style="color:rgb(13, 18, 57);">：分布式训练中梯度通信前转换数据类型（FP32 → FP16）。</font>
    - **<font style="color:rgb(13, 18, 57);">融合原因</font>**<font style="color:rgb(13, 18, 57);">：在通信前直接完成类型转换，减少单独内核启动的开销。</font>



<font style="color:rgb(13, 18, 57);">为什么需要算子融合？</font>

1. **<font style="color:rgb(13, 18, 57);">减少显存带宽压力</font>**<font style="color:rgb(13, 18, 57);">：中间结果无需写回显存，降低带宽需求。</font>
2. **<font style="color:rgb(13, 18, 57);">降低内核启动开销</font>**<font style="color:rgb(13, 18, 57);">：GPU 上每次内核启动有固定延迟，融合后减少次数。</font>
3. **<font style="color:rgb(13, 18, 57);">提高计算密度</font>**<font style="color:rgb(13, 18, 57);">：通过合并访存密集型与计算密集型操作，提升硬件利用率（如 GPU 的 SM 利用率）。</font>



<font style="color:rgb(13, 18, 57);">实际案例</font>

+ **<font style="color:rgb(13, 18, 57);">FlashAttention</font>**<font style="color:rgb(13, 18, 57);">：通过融合自注意力的矩阵乘、Softmax 和掩码，将显存占用从 O(N²) 降至 O(N)。</font>
+ **<font style="color:rgb(13, 18, 57);">DeepSpeed</font>**<font style="color:rgb(13, 18, 57);">：在分布式训练中融合通信与计算操作（如梯度 All-Reduce 与参数更新）。</font>
+ **<font style="color:rgb(13, 18, 57);">TensorRT</font>**<font style="color:rgb(13, 18, 57);">：在推理引擎中将卷积、BN、激活函数融合为单个内核（如 </font>`<font style="color:rgb(13, 18, 57);">Conv-BN-ReLU</font>`<font style="color:rgb(13, 18, 57);">）。</font>

:::

:::color5
14. **<font style="color:#601BDE;">flash attention的原理讲讲？你认为为什么flash attention极大提升了训练速度？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(51, 51, 51);">Fla</font><font style="color:#1f2329;">shAttention提供了⼀种⾼效且数值稳定的⾃注意⼒计算⽅法 ，通过优化内存访问和计算</font>

<font style="color:#1f2329;">流程，解决了传统⾃注意⼒在⻓序列处理中的</font>**<font style="color:#ED740C;">内存和计算瓶颈</font>**<font style="color:#1f2329;">。总结其优势：</font>

+ <font style="color:#1456f0;"></font><font style="color:#1f2329;">内存⾼效：⼤幅降低内存占⽤ ，适合处理⻓序列。</font>
+ <font style="color:#1f2329;">计算⾼效：减少访存开销 ，提⾼计算速度。</font>

**<font style="color:#117CEE;">问题本质</font>**

+ <font style="color:#de7802;">内存瓶颈</font><font style="color:#1f2329;">：GPU 的内存带宽限制了⾃注意⼒的计算速度。</font>
+ <font style="color:#de7802;">访存开销</font><font style="color:#1f2329;">：传统算法需要多次读取和写⼊ GPU 内存 ，导致⼤量的访存操作。</font>

**<font style="color:#117CEE;">核心思想</font>**

<font style="color:#1f2329;">FlashAttention</font><font style="color:#1f2329;">通过以下⽅式优化⾃注意⼒计算：</font>

+ <font style="color:#de7802;">块处理（ Blocking） </font><font style="color:#1f2329;">：将计算划分为⼩块 ，逐块处理，减少⼀次性需要的内存。</font>
+ <font style="color:#de7802;">IO 感知（IO-Awareness）</font><font style="color:#1f2329;">：优化内存访问模式，最⼤化数据在⾼速缓存中的使⽤ ，减少访存开销。</font>
+ <font style="color:#de7802;">数值稳定性</font><font style="color:#1f2329;">：在块内进⾏归⼀化 ，避免数值溢出。</font>

**<font style="color:#117CEE;">实现步骤</font>**

1. **<font style="color:#1f2329;">块划分</font>**<font style="color:#1f2329;">：将序列⻓度</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">划分为多个块，每个块的⼤⼩为</font>_<font style="color:#1f2329;">B </font>_<font style="color:#1f2329;">。例如，序列⻓度为 1024，块⼤⼩为 128，则有 8 个块。</font>
2. **<font style="color:#1f2329;">逐块计算</font>**
    - <font style="color:#1f2329;">计算块间的注意⼒：对于每个查询块和键块，计算局部的注意⼒值。</font>
    - <font style="color:#1f2329;">内存占⽤优化：只在寄存器或⾼速缓存中存储当前块的数据，避免将整个</font>_<font style="color:#1f2329;">L</font>_<font style="color:#1f2329;">× </font>_<font style="color:#1f2329;">L</font>_

<font style="color:#1f2329;">的注意⼒矩阵存⼊内存。</font>

3. **数值稳定的softmax计算**
    - <font style="color:#1f2329;">局部归⼀化：在块内进⾏Softmax 计算，使⽤数值稳定的算法，避免指数计算中的溢出。</font>
    - <font style="color:#1f2329;">累积计算：逐块累积注意⼒值和归⼀化因⼦，确保最终结果的准确性。</font>

:::

:::color5
15. **<font style="color:#601BDE;">paged attention的原理讲讲？你认为为什么paged attention极大提升了推理速度？它和flash attention的区别是什么？ </font>**<font style="color:#D22D8D;">(by草莓师姐)</font>

:::

:::success
**<font style="color:#74B602;">回答：</font>**

<font style="color:rgb(51, 51, 51);">Page Attention 是一种针对长序列处理优化的注意力机制，旨在降低传统自注意力的内存和计算开销，同时保持对长距离依赖的建模能力。其核心思想借鉴计算机系统中的</font>**<font style="color:#ED740C;">分页机制</font>**<font style="color:rgb(51, 51, 51);">，将输入序列分割为多个“页面”（块），动态管理这些块的计算和存储，从而优化资源使用。</font>

1. **传统自注意力瓶颈**  
Transformer的自注意力复杂度为O(N²)，在处理长序列时显存占用激增，尤其在大batch size下，成为训练/推理的主要瓶颈。
2. **分页管理思想**  
Page Attention将输入序列划分为固定大小的页面（Page），每个页面包含连续的token。计算注意力时：
    - **<font style="color:rgb(51, 51, 51);">页面内（Intra-Page）</font>**<font style="color:rgb(51, 51, 51);">：计算当前页面内所有token间的局部注意力。</font>
    - **<font style="color:rgb(51, 51, 51);">页面间（Inter-Page）</font>**<font style="color:rgb(51, 51, 51);">：按需加载其他页面，计算跨页面的稀疏注意力（如相邻页或关键页）。</font>
3. **动态加载机制**  
通过类似虚拟内存的换页策略，仅保留活跃页面在高速内存（如GPU显存）中，非活跃页面暂存于低速内存（如CPU内存或磁盘），按需动态交换，显著降低峰值显存占用。

:::

