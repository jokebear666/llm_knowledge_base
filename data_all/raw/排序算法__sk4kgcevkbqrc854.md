# 排序算法

<!-- source: yuque://zhongxian-iiot9/hlyypb/sk4kgcevkbqrc854 -->

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

