# ⓷ 海量数据排序

<!-- source: yuque://zhongxian-iiot9/hlyypb/gndi1g75b1xu0aiw -->

### 海量数据排序<font style="color:#D22D8D;">（by草莓师姐）</font>
:::color5
**<font style="color:#601BDE;">1.思路分析</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(13, 18, 57);">问题拆分</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">海量数据无法一次性加载到内存中，因此需要将数据分块处理。</font>
    - <font style="color:rgb(13, 18, 57);">每次只加载一部分数据到内存中进行排序，并将排序结果写入磁盘。</font>
    - <font style="color:rgb(13, 18, 57);">最后，将多个已排序的小文件合并成一个完整的有序文件。</font>
2. **<font style="color:rgb(13, 18, 57);">核心步骤</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">分块排序</font>**<font style="color:rgb(13, 18, 57);">：将数据分成若干小块，每块大小适配内存限制，对每个小块进行排序并保存到磁盘。</font>
    - **<font style="color:rgb(13, 18, 57);">多路归并</font>**<font style="color:rgb(13, 18, 57);">：使用最小堆（Min-Heap）或优先队列来合并多个已排序的小文件。</font>
3. **<font style="color:rgb(13, 18, 57);">使用堆的优势</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">堆是一种高效的数据结构，可以在</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">O</font><font style="color:rgb(13, 18, 57);">(</font><font style="color:rgb(13, 18, 57);">log</font><font style="color:rgb(13, 18, 57);">⁡</font><font style="color:rgb(13, 18, 57);">k</font><font style="color:rgb(13, 18, 57);">)</font>_<font style="color:rgb(13, 18, 57);">O</font>_<font style="color:rgb(13, 18, 57);">(</font><font style="color:rgb(13, 18, 57);">lo</font><font style="color:rgb(13, 18, 57);">g</font>_<font style="color:rgb(13, 18, 57);">k</font>_<font style="color:rgb(13, 18, 57);">)</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">的时间复杂度内插入和删除元素。</font>
    - <font style="color:rgb(13, 18, 57);">在多路归并过程中，堆可以帮助我们快速找到当前最小的元素。</font>

:::color5
**<font style="color:#601BDE;">2.解决方案</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

**<font style="color:rgb(13, 18, 57);">步骤 1：分块排序</font>**

1. <font style="color:rgb(13, 18, 57);">将原始数据分成若干小块，每块大小不超过内存限制。</font>
2. <font style="color:rgb(13, 18, 57);">对每个小块在内存中进行排序（可以使用快速排序、归并排序等）。</font>
3. <font style="color:rgb(13, 18, 57);">将排序后的每个小块写入磁盘，形成多个临时文件。</font>

**<font style="color:rgb(13, 18, 57);">步骤 2：多路归并</font>**

1. <font style="color:rgb(13, 18, 57);">打开所有已排序的临时文件，并从每个文件中读取第一个元素，将其放入一个最小堆中。</font>
2. <font style="color:rgb(13, 18, 57);">从堆中取出最小值（即堆顶元素），将其写入最终输出文件。</font>
3. <font style="color:rgb(13, 18, 57);">从该元素所属的文件中读取下一个元素，加入堆中。</font>
4. <font style="color:rgb(13, 18, 57);">重复上述过程，直到所有文件中的数据都被处理完毕。</font>

:::color5
**<font style="color:#601BDE;">3.代码实现</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

<font style="color:rgb(13, 18, 57);">以下是一个 Python 实现：</font>

```python
import heapq
import os

def sort_large_file(input_file, output_file, memory_limit):
    # Step 1: 分块排序
    temp_files = []
    with open(input_file, 'r') as f:
        while True:
            # 读取一块数据（不超过内存限制）
            lines = f.readlines(memory_limit)
            if not lines:
                break

            # 对这一块数据进行排序
            lines.sort(key=lambda x: int(x.strip()))

            # 将排序后的数据写入临时文件
            temp_file = f'temp_{len(temp_files)}.txt'
            temp_files.append(temp_file)
            with open(temp_file, 'w') as temp_f:
                temp_f.writelines(lines)

    # Step 2: 多路归并
    merge_sorted_files(temp_files, output_file)

    # 清理临时文件
    for temp_file in temp_files:
        os.remove(temp_file)

def merge_sorted_files(sorted_files, output_file):
    # 打开所有已排序的文件
    file_handlers = [open(file, 'r') for file in sorted_files]
    min_heap = []

    # 初始化堆：从每个文件中读取第一个元素
    for i, fh in enumerate(file_handlers):
        line = fh.readline()
        if line:
            value = int(line.strip())
            heapq.heappush(min_heap, (value, i))

    # 将堆中的最小值写入输出文件
    with open(output_file, 'w') as out_f:
        while min_heap:
            # 取出堆顶元素（当前最小值）
            smallest_value, file_index = heapq.heappop(min_heap)
            out_f.write(f'{smallest_value}\n')

            # 从对应的文件中读取下一个元素
            next_line = file_handlers[file_index].readline()
            if next_line:
                next_value = int(next_line.strip())
                heapq.heappush(min_heap, (next_value, file_index))

    # 关闭所有文件句柄
    for fh in file_handlers:
        fh.close()

# 示例调用
input_file = 'large_data.txt'  # 输入文件名
output_file = 'sorted_data.txt'  # 输出文件名
memory_limit = 1024 * 1024  # 内存限制，例如 1MB
sort_large_file(input_file, output_file, memory_limit)
```

:::color5
**<font style="color:#601BDE;">4.代码解析</font>**<font style="color:#D22D8D;">（by草莓师姐）</font>

:::

1. **<font style="color:rgb(13, 18, 57);">分块排序</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">使用</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">readlines(memory_limit)</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">控制每次读取的数据量不超过内存限制。</font>
    - <font style="color:rgb(13, 18, 57);">对每块数据进行排序后，将其写入一个临时文件。</font>
2. **<font style="color:rgb(13, 18, 57);">多路归并</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">使用</font><font style="color:rgb(13, 18, 57);"> </font>`<font style="color:rgb(13, 18, 57);">heapq</font>`<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">模块构建最小堆。</font>
    - <font style="color:rgb(13, 18, 57);">每次从堆中取出最小值，将其写入输出文件。</font>
    - <font style="color:rgb(13, 18, 57);">从对应文件中读取下一个元素并加入堆中，直到所有文件处理完毕。</font>
3. **<font style="color:rgb(13, 18, 57);">清理临时文件</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">归并完成后，删除所有临时文件以释放磁盘空间。</font>

:::color5
**<font style="color:#601BDE;">5.时空复杂度</font>**

:::

1. **<font style="color:rgb(13, 18, 57);">时间复杂度</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - **<font style="color:rgb(13, 18, 57);">分块排序</font>**<font style="color:rgb(13, 18, 57);">：假设总数据量为</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">，每块大小为</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);">，则需要</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">O</font><font style="color:rgb(13, 18, 57);">(</font><font style="color:rgb(13, 18, 57);">N</font><font style="color:rgb(13, 18, 57);">log</font><font style="color:rgb(13, 18, 57);">⁡</font><font style="color:rgb(13, 18, 57);">M</font><font style="color:rgb(13, 18, 57);">)</font>_<font style="color:rgb(13, 18, 57);">O</font>_<font style="color:rgb(13, 18, 57);">(</font>_<font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">lo</font><font style="color:rgb(13, 18, 57);">g</font>_<font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);">)</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">的时间。</font>
    - **<font style="color:rgb(13, 18, 57);">多路归并</font>**<font style="color:rgb(13, 18, 57);">：假设共有</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">个文件，每个文件平均长度为</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">L</font>_<font style="color:rgb(13, 18, 57);">L</font>_<font style="color:rgb(13, 18, 57);">，则归并的时间复杂度为</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">O</font><font style="color:rgb(13, 18, 57);">(</font><font style="color:rgb(13, 18, 57);">N</font><font style="color:rgb(13, 18, 57);">log</font><font style="color:rgb(13, 18, 57);">⁡</font><font style="color:rgb(13, 18, 57);">K</font><font style="color:rgb(13, 18, 57);">)</font>_<font style="color:rgb(13, 18, 57);">O</font>_<font style="color:rgb(13, 18, 57);">(</font>_<font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">lo</font><font style="color:rgb(13, 18, 57);">g</font>_<font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);">)</font><font style="color:rgb(13, 18, 57);">。</font>
    - <font style="color:rgb(13, 18, 57);">总体时间复杂度为</font><font style="color:rgb(13, 18, 57);"> </font><font style="color:rgb(13, 18, 57);">O</font><font style="color:rgb(13, 18, 57);">(</font><font style="color:rgb(13, 18, 57);">N</font><font style="color:rgb(13, 18, 57);">log</font><font style="color:rgb(13, 18, 57);">⁡</font><font style="color:rgb(13, 18, 57);">M</font><font style="color:rgb(13, 18, 57);">+</font><font style="color:rgb(13, 18, 57);">N</font><font style="color:rgb(13, 18, 57);">log</font><font style="color:rgb(13, 18, 57);">⁡</font><font style="color:rgb(13, 18, 57);">K</font><font style="color:rgb(13, 18, 57);">)</font>_<font style="color:rgb(13, 18, 57);">O</font>_<font style="color:rgb(13, 18, 57);">(</font>_<font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">lo</font><font style="color:rgb(13, 18, 57);">g</font>_<font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);">+</font>_<font style="color:rgb(13, 18, 57);">N</font>_<font style="color:rgb(13, 18, 57);">lo</font><font style="color:rgb(13, 18, 57);">g</font>_<font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);">)</font><font style="color:rgb(13, 18, 57);">。</font>
2. **<font style="color:rgb(13, 18, 57);">空间复杂度</font>**<font style="color:rgb(13, 18, 57);">：</font>
    - <font style="color:rgb(13, 18, 57);">主要由堆和临时文件决定，空间复杂度为 O(K+M)</font>_<font style="color:rgb(13, 18, 57);">O</font>_<font style="color:rgb(13, 18, 57);">(</font>_<font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);">+</font>_<font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);">)，其中 K</font>_<font style="color:rgb(13, 18, 57);">K</font>_<font style="color:rgb(13, 18, 57);"> 是文件数量，M</font>_<font style="color:rgb(13, 18, 57);">M</font>_<font style="color:rgb(13, 18, 57);"> 是内存限制。</font>



### <font style="color:rgb(51, 51, 51);">快速排序</font>
<font style="color:rgb(51, 51, 51);">快速排序是一种高效的排序算法，采用分治策略。</font>

```python
def quicksort(arr, low, high):
    if low < high:
        # 找到划分点，将数组分成两部分
        pivot_index = partition(arr, low, high)
        # 递归排序左边部分
        quicksort(arr, low, pivot_index - 1)
        # 递归排序右边部分
        quicksort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    # 选择最后一个元素作为基准（pivot）
    pivot = arr[high]
    i = low - 1  # 指向小于基准的部分的最后一个元素

    # 遍历整个数组，进行划分
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1  # 增加小于基准的部分的大小
            arr[i], arr[j] = arr[j], arr[i]  # 交换元素

    # 把基准放到中间合适的位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1  # 返回基准的位置

# 使用示例
if __name__ == "__main__":
    arr = [10, 7, 8, 9, 1, 5]
    quicksort(arr, 0, len(arr) - 1)
    print("排序后的数组:", arr)
```

+ **<font style="color:rgb(51, 51, 51);">时间复杂度</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">最优情况：O(n log n)（当每次划分能够将数组均匀分割）</font>
    - <font style="color:rgb(51, 51, 51);">最坏情况：O(n^2)（当数组已经是有序状态或者逆序状态，每次划分只减少一个元素）</font>
    - <font style="color:rgb(51, 51, 51);">平均情况：O(n log n)</font>
+ **<font style="color:rgb(51, 51, 51);">空间复杂度</font>**<font style="color:rgb(51, 51, 51);">:</font>
    - <font style="color:rgb(51, 51, 51);">O(1)：由于在原地进行排序，不需要额外的数组空间，仅使用了常量级的辅助空间来存放一些变量。因此空间复杂度为 O(1)。</font>

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 示例
arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print("快速排序结果:", sorted_arr)
```

<font style="color:rgb(51, 51, 51);">时间复杂度</font>

+ <font style="color:rgb(51, 51, 51);">最优时间复杂度：O(n log n)，当每次选择的基准元素能将数组均匀地分割时。</font>
+ <font style="color:rgb(51, 51, 51);">平均时间复杂度：O(n log n)，这是快速排序的期望时间复杂度。</font>
+ <font style="color:rgb(51, 51, 51);">最坏时间复杂度：O(n^2)，当数组已经是有序的，或者每次选择的基准元素都是最小或最大的元素时，会导致不均匀分割。</font>

<font style="color:rgb(51, 51, 51);">空间复杂度</font>

+ <font style="color:rgb(51, 51, 51);">空间复杂度：O(log n)，这是因为递归调用的栈空间。因为每次递归调用时，数组的大小大约是原来的一半，所以栈的深度最多是 O(log n)</font>

### <font style="color:rgb(51, 51, 51);">冒泡排序</font>
<font style="color:rgb(51, 51, 51);">冒泡排序是一种简单的排序算法，重复地走访要排序的元素，比较相邻元素并交换顺序不正确的元素。</font>

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 示例
arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = bubble_sort(arr)
print("冒泡排序结果:", sorted_arr)
```

### <font style="color:rgb(51, 51, 51);">选择排序</font>
<font style="color:rgb(51, 51, 51);">选择排序是一种简单直观的排序算法，它的基本思想是每次从未排序的部分中选择最小（或最大）元素放到已排序的部分。</font>

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# 示例
arr = [64, 25, 12, 22, 11]
sorted_arr = selection_sort(arr)
print("选择排序结果:", sorted_arr)
```

