# 🔥 大数据基础

<!-- source: yuque://zhongxian-iiot9/hlyypb/ruq7q4vwo67ea93s -->

| **维度** | **Hadoop** | **MapReduce** | **ODPS** |
| --- | --- | --- | --- |
| **<font style="color:rgb(51, 51, 51);">部署方式</font>** | <font style="color:rgb(51, 51, 51);">自建集群</font> | <font style="color:rgb(51, 51, 51);">内置于 Hadoop</font> | <font style="color:rgb(51, 51, 51);">阿里云全托管</font> |
| **<font style="color:rgb(51, 51, 51);">计算模型</font>** | <font style="color:rgb(51, 51, 51);">批处理（磁盘）</font> | <font style="color:rgb(51, 51, 51);">批处理（Map + Reduce）</font> | <font style="color:rgb(51, 51, 51);">批处理 + 交互式查询</font> |
| **<font style="color:rgb(51, 51, 51);">适用场景</font>** | <font style="color:rgb(51, 51, 51);">企业内网离线分析</font> | <font style="color:rgb(51, 51, 51);">大规模数据聚合</font> | <font style="color:rgb(51, 51, 51);">云上数据仓库与 AI 分析</font> |
| **<font style="color:rgb(51, 51, 51);">成本</font>** | <font style="color:rgb(51, 51, 51);">硬件 + 运维成本高</font> | <font style="color:rgb(51, 51, 51);">免费（开源）</font> | <font style="color:rgb(51, 51, 51);">按使用量付费</font> |
| **<font style="color:rgb(51, 51, 51);">扩展性</font>** | <font style="color:rgb(51, 51, 51);">需手动扩容节点</font> | <font style="color:rgb(51, 51, 51);">依赖 Hadoop 集群</font> | <font style="color:rgb(51, 51, 51);">自动弹性扩缩容</font> |


**<font style="color:rgb(51, 51, 51);">选型建议</font>**

+ **<font style="color:rgb(51, 51, 51);">中小型企业</font>**<font style="color:rgb(51, 51, 51);">：优先使用 ODPS，降低运维成本。</font>
+ **<font style="color:rgb(51, 51, 51);">敏感数据场景</font>**<font style="color:rgb(51, 51, 51);">：选择 Hadoop 私有化部署。</font>
+ **<font style="color:rgb(51, 51, 51);">实时处理需求</font>**<font style="color:rgb(51, 51, 51);">：结合 Flink 或 Spark Streaming。</font>

# <font style="color:rgb(0, 0, 0);">Hadoop</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">Hadoop 是分布式存储与计算的 </font>**<font style="color:rgb(51, 51, 51);">开源框架</font>**<font style="color:rgb(51, 51, 51);">，核心组件包括：</font>

+ **<font style="color:rgb(51, 51, 51);">HDFS（Hadoop Distributed File System）</font>**<font style="color:rgb(51, 51, 51);">：文件分块存储（默认 128MB/块），多副本冗余（默认3副本）。</font>
+ **<font style="color:rgb(51, 51, 51);">YARN（资源调度器）</font>**<font style="color:rgb(51, 51, 51);">：管理集群资源（CPU、内存），分配任务到节点。</font>
+ **<font style="color:rgb(51, 51, 51);">MapReduce</font>**<font style="color:rgb(51, 51, 51);">：分布式计算模型（后文单独解析）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">以词频统计（WordCount）为例：</font>

1. **<font style="color:rgb(51, 51, 51);">Input Splitting</font>**<font style="color:rgb(51, 51, 51);">：输入文件切分成多个 Split（如200MB文件切为2块）。</font>
2. **<font style="color:rgb(51, 51, 51);">Map阶段</font>**<font style="color:rgb(51, 51, 51);">：每个Mapper处理一个 Split，输出</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);"><word, 1></font>`<font style="color:rgb(51, 51, 51);"> </font><font style="color:rgb(51, 51, 51);">键值对。</font>
3. **<font style="color:rgb(51, 51, 51);">Shuffle & Sort</font>**<font style="color:rgb(51, 51, 51);">：相同 Key 的数据聚合到同一 Reducer。</font>
4. **<font style="color:rgb(51, 51, 51);">Reduce阶段</font>**<font style="color:rgb(51, 51, 51);">：Reducer 对相同 Key 的值求和，输出</font><font style="color:rgb(51, 51, 51);"> </font>`<font style="color:rgb(51, 51, 51);"><word, total></font>`<font style="color:rgb(51, 51, 51);">。</font>
5. **<font style="color:rgb(51, 51, 51);">Output</font>**<font style="color:rgb(51, 51, 51);">：结果写入 HDFS。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">高容错性（数据冗余存储）。</font>
    - <font style="color:rgb(51, 51, 51);">横向扩展性强（支持千节点集群）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">磁盘 I/O 开销大，速度慢。</font>
    - <font style="color:rgb(51, 51, 51);">实时性差，仅适合离线批处理。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">日志分析（如用户行为日志清洗）。</font>
+ <font style="color:rgb(51, 51, 51);">大规模数据 ETL（数据迁移、转换）。</font>
+ <font style="color:rgb(51, 51, 51);">历史数据归档存储。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">存储层</font>**<font style="color:rgb(51, 51, 51);">：使用 ORC/Parquet 列式存储提升压缩率和查询速度。</font>
+ **<font style="color:rgb(51, 51, 51);">计算层</font>**<font style="color:rgb(51, 51, 51);">：集成 Spark 替代 MapReduce 加速迭代计算。</font>
+ **<font style="color:rgb(51, 51, 51);">资源调度</font>**<font style="color:rgb(51, 51, 51);">：优化 YARN 配置，动态分配资源。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```python
// Mapper
public class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    public void map(LongWritable key, Text value, Context context) {
        String[] words = value.toString().split(" ");
        for (String word : words) {
            context.write(new Text(word), new IntWritable(1));
        }
    }
}

// Reducer
public class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context) {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        context.write(key, new IntWritable(sum));
    }
}

```



# <font style="color:rgb(0, 0, 0);">MapReduce</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">MapReduce 是 </font>**<font style="color:rgb(51, 51, 51);">分而治之</font>**<font style="color:rgb(51, 51, 51);"> 的分布式计算模型：</font>

+ **<font style="color:rgb(51, 51, 51);">Map</font>**<font style="color:rgb(51, 51, 51);">：将输入数据转换为键值对（</font>`<font style="color:rgb(51, 51, 51);"><K1, V1> → <K2, V2></font>`<font style="color:rgb(51, 51, 51);">）。</font>
+ **<font style="color:rgb(51, 51, 51);">Reduce</font>**<font style="color:rgb(51, 51, 51);">：对相同 Key 的值进行聚合（</font>`<font style="color:rgb(51, 51, 51);"><K2, List<V2>> → <K3, V3></font>`<font style="color:rgb(51, 51, 51);">）。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

1. **<font style="color:rgb(51, 51, 51);">InputFormat</font>**<font style="color:rgb(51, 51, 51);">：读取输入数据并分片。</font>
2. **<font style="color:rgb(51, 51, 51);">Mapper</font>**<font style="color:rgb(51, 51, 51);">：用户自定义处理逻辑。</font>
3. **<font style="color:rgb(51, 51, 51);">Combiner（可选）</font>**<font style="color:rgb(51, 51, 51);">：本地聚合减少网络传输。</font>
4. **<font style="color:rgb(51, 51, 51);">Partitioner</font>**<font style="color:rgb(51, 51, 51);">：决定数据分发到哪个 Reducer。</font>
5. **<font style="color:rgb(51, 51, 51);">Reducer</font>**<font style="color:rgb(51, 51, 51);">：全局聚合输出结果。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">简单易用，适合线性扩展的任务。</font>
    - <font style="color:rgb(51, 51, 51);">自动处理节点故障。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">中间数据需落盘，效率低。</font>
    - <font style="color:rgb(51, 51, 51);">不适合迭代计算（如机器学习训练）。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">批量数据清洗（如去重、过滤）。</font>
+ <font style="color:rgb(51, 51, 51);">聚合统计（如 PV/UV 计算）。</font>
+ <font style="color:rgb(51, 51, 51);">分布式排序（如海量数据 Top-N 查询）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">内存计算</font>**<font style="color:rgb(51, 51, 51);">：使用 Spark RDD 替代 MapReduce。</font>
+ **<font style="color:rgb(51, 51, 51);">优化 Shuffle</font>**<font style="color:rgb(51, 51, 51);">：压缩中间数据，减少网络传输。</font>
+ **<font style="color:rgb(51, 51, 51);">推测执行</font>**<font style="color:rgb(51, 51, 51);">：防止慢节点拖累整体任务。</font>



# <font style="color:rgb(0, 0, 0);">ODPS</font>
:::color3
**<font style="color:rgb(51, 51, 51);">简介</font>**<font style="color:rgb(51, 51, 51);">：</font><font style="color:rgb(51, 51, 51);">ODPS 是阿里云的 </font>**<font style="color:rgb(51, 51, 51);">全托管大数据平台</font>**<font style="color:rgb(51, 51, 51);">，核心特性：</font>

+ **<font style="color:rgb(51, 51, 51);">存储层</font>**<font style="color:rgb(51, 51, 51);">：分布式表存储（支持结构化/半结构化数据）。</font>
+ **<font style="color:rgb(51, 51, 51);">计算层</font>**<font style="color:rgb(51, 51, 51);">：提供 SQL、MapReduce、Graph 等多种计算模型。</font>
+ **<font style="color:rgb(51, 51, 51);">资源调度</font>**<font style="color:rgb(51, 51, 51);">：按需分配资源，按量计费。</font>

:::

:::color5
**<font style="color:#601BDE;">1.计算步骤</font>**

:::

<font style="color:rgb(51, 51, 51);">以 SQL 查询为例：</font>

1. **<font style="color:rgb(51, 51, 51);">创建表</font>**<font style="color:rgb(51, 51, 51);">：定义表结构和存储格式。</font>
2. **<font style="color:rgb(51, 51, 51);">导入数据</font>**<font style="color:rgb(51, 51, 51);">：通过 Tunnel 命令或 DataWorks 上传数据。</font>
3. **<font style="color:rgb(51, 51, 51);">执行 SQL</font>**<font style="color:rgb(51, 51, 51);">：编写 SQL 进行查询或聚合。</font>
4. **<font style="color:rgb(51, 51, 51);">导出结果</font>**<font style="color:rgb(51, 51, 51);">：将结果表导出到 OSS 或本地。</font>

:::color5
**<font style="color:#601BDE;">2.优缺点</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">优点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">免运维，弹性扩缩容。</font>
    - <font style="color:rgb(51, 51, 51);">集成阿里云生态（DataWorks、PAI）。</font>
+ **<font style="color:rgb(51, 51, 51);">缺点</font>**<font style="color:rgb(51, 51, 51);">：</font>
    - <font style="color:rgb(51, 51, 51);">计算延迟高于 Spark/Flink。</font>
    - <font style="color:rgb(51, 51, 51);">SQL 语法与标准略有差异。</font>

:::color5
**<font style="color:#601BDE;">3.应用场景</font>**

:::

+ <font style="color:rgb(51, 51, 51);">数据仓库构建（企业级数仓）。</font>
+ <font style="color:rgb(51, 51, 51);">机器学习模型训练（配合 PAI）。</font>
+ <font style="color:rgb(51, 51, 51);">实时离线一体化分析（结合 Hologres）。</font>

:::color5
**<font style="color:#601BDE;">4.改进方法</font>**

:::

+ **<font style="color:rgb(51, 51, 51);">数据分区</font>**<font style="color:rgb(51, 51, 51);">：按时间或业务键分区，减少扫描量。</font>
+ **<font style="color:rgb(51, 51, 51);">优化 SQL</font>**<font style="color:rgb(51, 51, 51);">：避免全表扫描，使用索引或列裁剪。</font>
+ **<font style="color:rgb(51, 51, 51);">资源调优</font>**<font style="color:rgb(51, 51, 51);">：调整 CU（计算单元）数量平衡速度与成本。</font>

:::color5
**<font style="color:#601BDE;">5.实现代码示例</font>**

:::

```sql
-- 创建表
CREATE TABLE user_logs (
  user_id STRING,
  action_time DATETIME,
  action_type STRING
) PARTITIONED BY (dt STRING);

-- 查询每日活跃用户数
INSERT OVERWRITE TABLE daily_active_users
SELECT dt, COUNT(DISTINCT user_id) AS active_users
FROM user_logs
WHERE dt >= '2023-10-01' AND action_type = 'login'
GROUP BY dt;

```



<font style="color:rgb(0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);">MapReduce揭秘：4步搞定</font>  
<font style="color:rgb(0, 0, 0);">嘿，朋友们！今天我们来聊聊MapReduce和Hadoop，这两个在大数据处理中超级重要的概念。别担心，我会尽量用大白话来解释，保证你一看就懂！</font><font style="color:rgb(0, 0, 0);">😉</font>  
<font style="color:rgb(0, 0, 0);">什么是Hadoop？</font>  
<font style="color:rgb(0, 0, 0);">Hadoop是Apache基金会的一个开源项目，用Java语言写的。它是一个开发和运行处理大规模数据的软件平台。简单来说，Hadoop允许你用简单的编程模型在大量计算机集群上对大型数据集进行分布式处理。</font>  
<font style="color:rgb(0, 0, 0);">Hadoop的核心组件</font>  
<font style="color:rgb(0, 0, 0);">Hadoop的核心组件包括：</font>  
<font style="color:rgb(0, 0, 0);">HDFS（分布式文件系统）：解决海量数据存储问题。</font>  
<font style="color:rgb(0, 0, 0);">Map/Reduce（分布式运算编程框架）：解决海量数据计算问题。</font>  
<font style="color:rgb(0, 0, 0);">YARN（作业调度和集群资源管理框架）：解决资源任务调度问题。</font>  
<font style="color:rgb(0, 0, 0);">MapReduce的工作原理</font>  
<font style="color:rgb(0, 0, 0);">MapReduce程序的工作分为两个阶段：</font>  
<font style="color:rgb(0, 0, 0);">Map阶段（分割、映射）：这个阶段会把输入的数据分割成小块，然后对每个小块进行映射操作。</font>  
<font style="color:rgb(0, 0, 0);">Reduce阶段（重排、还原）：这个阶段会把Map阶段的输出进行排序和合并，最终得到结果。</font>  
<font style="color:rgb(0, 0, 0);">实例：用MapReduce统计单词数量</font>  
<font style="color:rgb(0, 0, 0);">假设我们有以下的输入数据：</font>  
<font style="color:rgb(0, 0, 0);">Welcome to Hadoop Class</font>  
<font style="color:rgb(0, 0, 0);">Hadoop is good</font>  
<font style="color:rgb(0, 0, 0);">Hadoop is bad</font>  
  
<font style="color:rgb(0, 0, 0);">我们需要统计这段文字中各单词的数量。MapReduce的工作流程如下：</font>  
<font style="color:rgb(0, 0, 0);">输入拆分（Input splits）：JobClient会把数据划分成固定大小的块（input splits）。在我们的例子中，这段文字被分割成了4个小句。</font>  
<font style="color:rgb(0, 0, 0);">映射（Mapping）：每个分割的数据会根据Map映射函数产生输出值。在这个例子中，映射阶段的任务就是计算每个小句中每个单词的数量。</font>  
<font style="color:rgb(0, 0, 0);">重排（Shuffling）：这个阶段是最重要的部分。shuffle得到map的输出后，进行分区操作，把相同Key的key/value对输入到相同reduce中。在我们的例子中，key就是单词，value就是出现次数，这个阶段把同样的单词分在了一起。</font>  
<font style="color:rgb(0, 0, 0);">Reduce（Reducing）：reduce读入shuffle的输出后，对value的集合进行reduce操作，也就是对输出值汇总。等所有的reduce完成后，返回一个输出值。总结来说，这一阶段汇总了完整的数据集。在我们的例子中，即计算每个单词出现次数的总和。</font>  
<font style="color:rgb(0, 0, 0);">总结</font>  
<font style="color:rgb(0, 0, 0);">一句话总结MapReduce：一个MapReduce作业通常会把输入的数据集切分为若干独立的数据块，由map任务以完全并行的方式处理它们。框架会对map的输出先进行排序，然后把结果输入给reduce任务。</font>  
  
<font style="color:rgb(0, 0, 0);">MapReduce框架是整个Hadoop框架的核心，实现了大数据的分布式处理，从而提高了输出处理的效率。希望这篇文章能帮你更好地理解MapReduce和Hadoop！</font><font style="color:rgb(0, 0, 0);">📚</font>

