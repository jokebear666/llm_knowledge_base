# 📕 LeetCode Hot100

<!-- source: yuque://zhongxian-iiot9/hlyypb/gw6bwrxhmfdlbici -->

# 一、数组
## 1.1 一维数组
### 二分查找
二分法要求<font style="color:#DF2A3F;">数组有序</font>。

输入数组nums和target，输出目标的下标

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2  # 避免大数相加导致的溢出

        # 检查中间值是否是目标值
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1  # 在右侧继续搜索
        else:
            right = mid - 1  # 在左侧继续搜索

    return -1  # 未找到目标值

# 示例用法
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 7
result = binary_search(nums, target)

print(f"目标值 {target} 的索引是: {result}")  # 输出：目标值 7 的索引是: 6
```

<font style="color:rgb(51, 51, 51);">时间复杂度为 O(logn)</font>

<font style="color:rgb(51, 51, 51);">空间复杂度O(1)：只使用了常量级别的额外空间（即几个变量），不随输入规模的变化而变化</font>

### 两个正序数组的中位数（二分）
双指针+枚举。优化：二分法

<font style="color:rgb(38, 38, 38);">给定两个大小分别为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">m</font>`<font style="color:rgb(38, 38, 38);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);">n</font>`<font style="color:rgb(38, 38, 38);"> 的正序（从小到大）数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums1</font>`<font style="color:rgb(38, 38, 38);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums2</font>`<font style="color:rgb(38, 38, 38);">。请你找出并返回这两个正序数组的 </font>**<font style="color:rgb(38, 38, 38);">中位数</font>**<font style="color:rgb(38, 38, 38);"> 。算法的时间复杂度应该为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">O(log (m+n))</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734660439315-d749ce37-69d6-44fd-b55f-aa40c26ed9e4.png)

```python
class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        if len(a) > len(b):
            a, b = b, a  # 保证下面的 i 可以从 0 开始枚举

        m, n = len(a), len(b)
        a = [-inf] + a + [inf]
        b = [-inf] + b + [inf]

        # 枚举 nums1 有 i 个数在第一组
        # 那么 nums2 有 (m + n + 1) // 2 - i 个数在第一组
        i, j = 0, (m + n + 1) // 2
        while True:
            if a[i] <= b[j + 1] and a[i + 1] > b[j]:  # 写 >= 也可以
                max1 = max(a[i], b[j])  # 第一组的最大值
                min2 = min(a[i + 1], b[j + 1])  # 第二组的最小值
                return max1 if (m + n) % 2 else (max1 + min2) / 2
            i += 1  # 继续枚举
            j -= 1

```

时间复杂度：O(m+n)，其中 m 是 a 的长度，n 是 b 的长度。往 a 前面插入一个元素的时间复杂度是 O(m)，往 b 前面插入一个元素的时间复杂度是 O(n)，加起来是 O(m+n)。

空间复杂度：O(m+n)。

### 盛水最多的容器
:::color3
<font style="color:rgb(38, 38, 38);">给定一个长度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">n</font>`<font style="color:rgb(38, 38, 38);"> 的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">height</font>`<font style="color:rgb(38, 38, 38);"> 。有 </font>`<font style="color:rgba(38, 38, 38, 0.75);">n</font>`<font style="color:rgb(38, 38, 38);"> 条垂线，第 </font>`<font style="color:rgba(38, 38, 38, 0.75);">i</font>`<font style="color:rgb(38, 38, 38);"> 条线的两个端点是 </font>`<font style="color:rgba(38, 38, 38, 0.75);">(i, 0)</font>`<font style="color:rgb(38, 38, 38);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);">(i, height[i])</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

<font style="color:rgb(38, 38, 38);">找出其中的两条线，使得它们与 </font>`<font style="color:rgba(38, 38, 38, 0.75);">x</font>`<font style="color:rgb(38, 38, 38);"> 轴共同构成的容器可以容纳最多的水。</font>

<font style="color:rgb(38, 38, 38);">返回容器可以储存的最大水量。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">说明：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你不能倾斜容器。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734951120606-22f81903-f54e-4470-9ff9-f4d67f525fd2.png)

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        i = 0
        j = len(height) - 1
        res = 0
        while i < j :
            if height[i] < height[j]:
                res = max(res, min(height[i], height[j]) * (j-i))
                i += 1
            else:
                res = max(res, min(height[i], height[j]) * (j-i))
                j -= 1
        
        return res
```

+ **<font style="background-color:rgb(240, 240, 240);">时间复杂度</font>****<font style="background-color:rgb(240, 240, 240);"> </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>****<font style="background-color:rgb(240, 240, 240);"> ：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">双指针遍历一次底边宽度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>
+ **<font style="background-color:rgb(240, 240, 240);">空间复杂度 </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font>****<font style="background-color:rgb(240, 240, 240);"> ：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 变量 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> , </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> , </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">res</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 使用常数额外空间。</font>





### [删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)
**<font style="color:#601BDE;">解法：双指针</font>**

:::color3
<font style="color:rgb(38, 38, 38);">给你一个 </font>**<font style="color:rgb(38, 38, 38);">非严格递增排列</font>**<font style="color:rgb(38, 38, 38);"> 的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> ，请你</font>[**<font style="color:rgb(38, 38, 38);">原地</font>**](http://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)<font style="color:rgb(38, 38, 38);"> 删除重复出现的元素，使每个元素 </font>**<font style="color:rgb(38, 38, 38);">只出现一次</font>**<font style="color:rgb(38, 38, 38);"> ，返回删除后数组的新长度。元素的 </font>**<font style="color:rgb(38, 38, 38);">相对顺序</font>**<font style="color:rgb(38, 38, 38);"> 应该保持 </font>**<font style="color:rgb(38, 38, 38);">一致</font>**<font style="color:rgb(38, 38, 38);"> 。然后返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 中唯一元素的个数。</font>

<font style="color:rgb(38, 38, 38);">考虑</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的唯一元素的数量为</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，你需要做以下事情确保你的题解可以被通过：</font>

+ <font style="color:rgb(38, 38, 38);">更改数组</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，使</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的前</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">个元素包含唯一元素，并按照它们最初在</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">中出现的顺序排列。</font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 的其余元素与</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的大小不重要。</font>
+ <font style="color:rgb(38, 38, 38);">返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

:::

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        
        n = len(nums)
        left, right = 0, 1
        flag = 0
        while right < n:
            #右指针移动，直到找到下一个数字
            while nums[right-1] == nums[right] : 
                right += 1
                if right >= n :
                    flag = 1
                    break
            # 右指针走完
            if flag == 1:
                break
            else:
                left += 1
                nums[left] = nums[right]
                right += 1
        
        return left+1
```

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        
        n = len(nums)
        fast = slow = 1
        while fast < n:
            if nums[fast] != nums[fast - 1]:
                nums[slow] = nums[fast]
                slow += 1
            fast += 1
        
        return slow

```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是数组的长度。快指针和慢指针最多各移动</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">次。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。只需要使用常数的额外空间。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">移除元素</font>](https://leetcode.cn/problems/remove-element/)
**解法：双指针**

:::color3
<font style="color:rgb(38, 38, 38);">给你一个数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`_<font style="color:rgb(38, 38, 38);"> </font>_<font style="color:rgb(38, 38, 38);">和一个值 </font>`<font style="color:rgba(38, 38, 38, 0.75);">val</font>`<font style="color:rgb(38, 38, 38);">，你需要 </font>[**<font style="color:rgb(38, 38, 38);">原地</font>**](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)<font style="color:rgb(38, 38, 38);"> 移除所有数值等于 </font>`<font style="color:rgba(38, 38, 38, 0.75);">val</font>`_<font style="color:rgb(38, 38, 38);"> </font>_<font style="color:rgb(38, 38, 38);">的元素。元素的顺序可能发生改变。然后返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 中与 </font>`<font style="color:rgba(38, 38, 38, 0.75);">val</font>`<font style="color:rgb(38, 38, 38);"> 不同的元素的数量。</font>

<font style="color:rgb(38, 38, 38);">假设</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">中不等于</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">val</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的元素数量为</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);">，要通过此题，您需要执行以下操作：</font>

+ <font style="color:rgb(38, 38, 38);">更改</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">数组，使</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的前</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">个元素包含不等于</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">val</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的元素。</font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的其余元素和</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的大小并不重要。</font>
+ <font style="color:rgb(38, 38, 38);">返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);">。</font>

:::

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        left, right = 0, 0

        while right < n:
            if nums[right] != val:
                nums[left] = nums[right]
                left += 1
            right += 1
        
        return left
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为序列的长度。我们只需要遍历该序列至多两次。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。我们只需要常数的空间保存若干变量。</font>





### [搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)（二分）
**解法：二分法**

:::color3
<font style="color:rgb(38, 38, 38);">整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 按升序排列，数组中的值 </font>**<font style="color:rgb(38, 38, 38);">互不相同</font>**<font style="color:rgb(38, 38, 38);"> 。</font>

<font style="color:rgb(38, 38, 38);">在传递给函数之前，</font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">在预先未知的某个下标</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);">（</font>`<font style="color:rgba(38, 38, 38, 0.75);">0 <= k < nums.length</font>`<font style="color:rgb(38, 38, 38);">）上进行了</font><font style="color:rgb(38, 38, 38);"> </font>**<font style="color:rgb(38, 38, 38);">旋转</font>**<font style="color:rgb(38, 38, 38);">，使数组变为</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]</font>`<font style="color:rgb(38, 38, 38);">（下标</font><font style="color:rgb(38, 38, 38);"> </font>**<font style="color:rgb(38, 38, 38);">从 0 开始</font>**<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">计数）。例如，</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">[0,1,2,4,5,6,7]</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">在下标</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">3</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">处经旋转后可能变为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">[4,5,6,7,0,1,2]</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">。</font>

<font style="color:rgb(38, 38, 38);">给你</font><font style="color:rgb(38, 38, 38);"> </font>**<font style="color:rgb(38, 38, 38);">旋转后</font>**<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的数组</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">和一个整数</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">target</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，如果</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">中存在这个目标值</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">target</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，则返回它的下标，否则返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">-1</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

<font style="color:rgb(38, 38, 38);">你必须设计一个时间复杂度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">O(log n)</font>`<font style="color:rgb(38, 38, 38);"> 的算法解决此问题。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
```

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        '''
        将数组一分为二，其中一定有一个是有序的，另一个可能是有序，也能是部分有序。
        此时有序部分用二分法查找。无序部分再一分为二，其中一个一定有序，另一个可能有序，可能无序。就这样循环.
        '''
        l, r = 0, len(nums) - 1
        while l <= r:
            mid = (l+r)//2
            if nums[mid] == target:
                return mid
            #如果[0, mid]有序
            if nums[0] <= nums[mid]:
                #如果目标在[0, mid]中
                if nums[0] <= target < nums[mid]:
                    r = mid - 1
                #如果目标不在[0, mid]中,则在[mid, n]中
                else:
                    l = mid + 1
            #如果[mid, n]有序
            else:
                #如果目标在[mid, n]中
                if nums[mid] < target <= nums[len(nums)-1]:
                    l = mid + 1
                # 如果目标不在[mid, n]中， 则在[0, mid]中
                else:
                    r = mid - 1
```



### [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)（二分）
**<font style="color:#601BDE;">解法：两次二分法</font>**

:::color3
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个按照非递减顺序排列的整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，和一个目标值</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。请你找出给定目标值在数组中的开始位置和结束位置。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果数组中不存在目标值</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[-1, -1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你必须设计并实现时间复杂度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(log n)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的算法解决此问题。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
```

```python
# @lc code=start
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        left, right = 0, n-1
        first, last = -1, -1
        
        #找第一个位置
        while left <= right:
            mid = (left+right) // 2
            if nums[mid] == target:
                first = mid
                right = mid - 1 #右指针左移
            elif nums[mid] > target:
                right = mid - 1
            else:
                left  = mid + 1
        
         #找最后位置
        left, right = 0, n-1
        while left <= right:
            mid = (left+right) // 2
            if nums[mid] == target:
                last = mid
                left = mid + 1 #左指针右移
            elif nums[mid] > target:
                right = mid - 1
            else:
                left  = mid + 1
        
        return [first, last]
```

时间复杂度： O(logn) ，其中 n 为数组的长度。二分查找的时间复杂度为 O(logn)，一共会执行两次，因此总时间复杂度为 O(logn)。

空间复杂度：O(1) 。只需要常数空间存放若干变量。



### [接雨水](https://leetcode.cn/problems/trapping-rain-water/)
动态规划/双指针

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个非负整数表示每个宽度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1735893536298-610bbaf6-559d-469f-92e8-fa6b564a1363.png)

```plain
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：height = [4,2,0,3,2,5]
输出：9
```

对于下标 i：

下雨后水能到达的最大高度：等于下标 i 两边的最大高度的最小值

下标 i 处能接的雨水量：等于下标 i 处的水能到达的最大高度减去 height[i]。

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        left, right = 0, n-1
        leftmax, rightmax = 0, 0
        ans = 0
        while left <= right:
            #更新两个最大值
            leftmax = max(leftmax, height[left])
            rightmax = max(rightmax, height[right])
            #如果左最大值 < 右最大值 下标 left 处能接的雨水量等于 leftMax−height[left]，将下标 left 处能接的雨水量加到能接的雨水总量，然后将 left 加 1（即向右移动一位）；
            if leftmax < rightmax:
                ans += leftmax - height[left]
                left += 1
            #如果左最大值 >= 右最大值 下标 right 处能接的雨水量等于 rightMax−height[right]，将下标 right 处能接的雨水量加到能接的雨水总量，然后将 right 减 1（即向左移动一位）。
            else:
                ans += rightmax - height[right]
                right -= 1
            
        return ans
```

+ 时间复杂度：O(n)，其中 n 是数组 height 的长度。计算数组 leftMax 和 rightMax 的元素值各需要遍历数组 height 一次，计算能接的雨水总量还需要遍历一次。
+ 空间复杂度：O(n)，其中 n 是数组 height 的长度。需要创建两个长度为 n 的数组 leftMax 和 rightMax。



15. [**<font style="background-color:rgb(240, 240, 240);">跳跃游戏</font>**](https://leetcode.cn/problems/jump-game/)

<font style="background-color:rgb(240, 240, 240);">贪心</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个非负整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，你最初位于数组的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">第一个下标</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。数组中的每个元素代表你在该位置可以跳跃的最大长度。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">判断你是否能够到达最后一个下标，如果可以，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。
```

```python
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        n = len(nums)
        right_pos = 0
        # 依次遍历数组中的每一个位置，并实时维护 最远可以到达的位置。
        # 对于当前遍历到的位置 x，
        for i in range(n):
            # 如果它在 最远可以到达的位置 的范围内，那么我们就可以从起点通过若干次跳跃到达该位置，
            # 因此我们可以用 x+nums[x] 更新 最远可以到达的位置。
            if right_pos >= i:
                right_pos = max(right_pos, i + nums[i])
            #如果 最远可以到达的位置 大于等于数组中的最后一个位置，那就说明最后一个位置可达
            if right_pos >= n-1:
                return True
        return False
                
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为数组的大小。只需要访问</font><font style="background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">数组一遍，共</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">个位置。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">，不需要额外的空间开销。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [颜色分类（75）](https://leetcode.cn/problems/sort-colors/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个包含红色、白色和蓝色、共 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个元素的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，</font>[**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">原地</font>**](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">我们使用整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">分别表示红色、白色和蓝色。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">必须在不使用库内置的 sort 函数的情况下解决这个问题。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [2,0,1]
输出：[0,1,2]
```

```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        ptr = 0
        n = len(nums)
        #第一次遍历，把所有的0放在开头
        for i in range(n):
            if nums[i] == 0:
                tmp = nums[i]
                nums[i] = nums[ptr]
                nums[ptr] = tmp
                ptr += 1
        #第二次遍历，把所有的1放在开头（在所有0后面）
        for i in range(n):
            if nums[i] == 1:
                tmp = nums[i]
                nums[i] = nums[ptr]
                nums[ptr] = tmp
                ptr += 1
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是数组</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">的长度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">买卖股票的最佳时机（121）</font>](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，它的第 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个元素 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示一支给定股票第</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">天的价格。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你只能选择</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">某一天</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">买入这只股票，并选择在</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">未来的某一个不同的日子</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">卖出该股票。设计一个算法来计算你所能获取的最大利润。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
```

只需要遍历价格数组一遍，记录历史最低点，然后在每一天考虑这么一个问题：如果我是在历史最低点买进的，那么我今天卖出能赚多少钱？当考虑完所有天数之时，我们就得到了最好的答案。

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # #暴力，超出时限
        # res = 0
        # for i in range(len(prices)-1):
        #     for j in range(i+1, len(prices)):
        #         res = max(res, prices[j]-prices[i])
        # return res        
        
        n = len(prices)
        res = 0
        left_min = inf
        left, right = 0, 1
        while right < n:
            #左指针，寻找right左侧的最小值
            while left < right:
                left_min = min(left_min, prices[left])
                left += 1
                
            res = max(res, prices[right]-left_min)
            
            #右移右指针
            right += 1

        return res
```

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        #一次遍历
        n = len(prices)
        res = 0
        left_min = prices[0]
        for i in range(1, n):
            left_min = min(left_min, prices[i-1])
            res = max(res, prices[i]-left_min)
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，只需要遍历一次。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，只使用了常数个变量。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">买卖股票的最佳时机 II（122）</font>](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示某支股票第</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">天的价格。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在每一天，你可以决定是否购买和/或出售股票。你在任何时候 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最多</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 只能持有</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一股</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">股票。你也可以先购买，然后在</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">同一天</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">出售。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你能获得的 </font>__**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最大</font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 利润</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：prices = [7,1,5,3,6,4]
输出：7
解释：在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4。
随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6 - 3 = 3。
最大总利润为 4 + 3 = 7 。
```

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        
        res = 0
        
        for i in range(1, len(prices)):
            #累加所有的上坡处利润
            if prices[i] > prices[i-1]:
                tmp = prices[i] - prices[i-1]
                res += tmp
        
        return res
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为数组的长度。我们只需要遍历一次数组即可。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。只需要常数空间存放若干变量。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [买卖股票的最佳时机含冷冻期（309）](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个整数数组</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中第 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prices[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 表示第 </font>`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>_`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 天的股票价格 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">设计一个算法计算出最大利润。在满足以下约束条件下，你可以尽可能地完成更多的交易（多次买卖一支股票）:</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">卖出股票后，你无法在第二天买入股票 (即冷冻期为 1 天)。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: prices = [1,2,3,0,2]
输出: 3 
解释: 对应的交易状态为: [买入, 卖出, 冷冻期, 买入, 卖出]
```

have[i] 表示第i天持有股票所得最多现金

no[i] 表示第i天不持有股票且不处于冷冻期所得最多现金

cold[i] 表示第i天不持有股票且处于冷冻期所得最多现金

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736753489947-9c8a7f9c-fc2f-4dfd-bed5-946f8bbea2eb.png)

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        if n <= 1 :
            return 0
        #have[i] 表示第i天持有股票所得最多现金
        have = [0] * n
        #no[i] 表示第i天不持有股票且不处于冷冻期所得最多现金
        no = [0] * n
        have[0] = - prices[0]
        no[0] = 0     
        have[1] = max(have[0], -prices[1])
        no[1] = max(no[0], have[0] + prices[1])
        for i in range(2, n) :
            #第i-i天不持有股票且不在冷冻期，则保持现状，所得现金是no[i-1]
            #第i-i天不持有股票且在冷冻期，则第i天在冷静期，所得现金是cold[i-1]
            #cold[i-1]含义是第i-1天持有股票且卖出股票，则第i天是冷静期，cold[i-1] = have[i-1] + prices[i]
            no[i] = max(no[i - 1], have[i - 1] + prices[i])
            #第i-1天持有股票，则第i天保持现状，所得现金是have[i-1]
            #第i-i天买入股票，所得现金是昨天不持有股票 且 不处于冷冻期的所得现金，减去今天股票价格 no[i-2]-prices[i]
            have[i] = max(have[i - 1], no[i - 2] - prices[i])
        
        return no[n - 1]
```

### [<font style="background-color:rgb(240, 240, 240);">只出现一次的数字（136）</font>](https://leetcode.cn/problems/single-number/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非空</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1 ：</font>**

```plain
输入：nums = [2,2,1]
输出：1
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2 ：</font>**

```plain
输入：nums = [4,1,2,1,2]
输出：4
```

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        #哈希表
        hashmap = dict()
        for num in nums:
            if num not in hashmap:
                hashmap[num] = 1
            else:
                hashmap[num] += 1
        
        for key, value in hashmap.items():
            if value == 1:
                return key
        
        return None
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(n)</font><font style="background-color:rgb(240, 240, 240);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736327001544-70853f91-dfd6-4499-a3d4-a2501f2724d7.png)

```python
class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        x = 0
        for num in nums:  # 1. 遍历 nums 执行异或运算
            x ^= num      
        return x;         # 2. 返回出现一次的数字 x

```

时间复杂度 O(N) ： 线性遍历 nums 使用 O(N) 时间，异或操作使用 O(1) 时间。

空间复杂度 O(1) ： 辅助变量 a , b , x , y 使用常数大小额外空间。



### [<font style="background-color:rgb(240, 240, 240);">数组中的第 K 个最大元素（215）</font>](https://leetcode.cn/problems/xx4gT2/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请返回数组中第</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>**`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个最大的元素。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请注意，你需要找的是数组排序后的第 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个最大的元素，而不是第 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个不同的元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [3,2,1,5,6,4], k = 2
输出：5
```

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 获取数组长度
        n = len(nums)
        # 初始化左右边界
        l = 0
        r = n - 1
        
        # 循环进行快速排序的分区，直到找到第k大的数字
        while True:
            # 调用partition函数进行分区，并获取分区后pivot的索引
            idx = self.partition(nums, l, r)
            # 如果当前idx正好是我们想要的第k-1个元素（因为索引是从0开始的）
            if idx == k - 1:
                # 返回当前的第k大的元素
                return nums[idx]
            # 如果idx小于k-1，说明第k大的元素在右侧部分
            elif idx < k - 1:
                l = idx + 1  # 更新左边界
            # 如果idx大于k-1，说明第k大的元素在左侧部分
            else:
                r = idx - 1  # 更新右边界


    #----用于快速排序的分区函数
    def partition(self, nums: List[int], l: int, r: int) -> int:
        # 选择数组的第一个元素作为pivot（基准值）
        pivot = nums[l]
        # 记录pivot的初始位置
        begin = l
        
        # 执行分区操作，直到左边界和右边界相遇
        while l < r:
            # 右边的指针向左移动，直到找到一个大于pivot的元素
            while l < r and nums[r] <= pivot:
                r -= 1
            # 左边的指针向右移动，直到找到一个小于pivot的元素
            while l < r and nums[l] >= pivot:
                l += 1
            # 如果左指针没有相遇，则交换这两个元素
            if l < r:
                nums[l], nums[r] = nums[r], nums[l]
        
        # 将pivot放到它的最终位置
        nums[begin], nums[l] = nums[l], nums[begin]
        # 返回pivot最终的位置索引
        return l
```

```python
class Solution:
    def findKthLargest(self, nums, k):
        def quick_select(nums, k):
            # 随机选择基准数
            pivot = random.choice(nums)
            big, equal, small = [], [], []
            # 将大于、小于、等于 pivot 的元素划分至 big, small, equal 中
            for num in nums:
                if num > pivot:
                    big.append(num)
                elif num < pivot:
                    small.append(num)
                else:
                    equal.append(num)
            if k <= len(big):
                # 第 k 大元素在 big 中，递归划分
                return quick_select(big, k)
            if len(nums) - len(small) < k:
                # 第 k 大元素在 small 中，递归划分
                return quick_select(small, k - len(nums) + len(small))
            # 第 k 大元素在 equal 中，直接返回 pivot
            return pivot
        
        return quick_select(nums, k)


```

思路

应用快速排序，使用的是快速选择方法，没有必要全部排序，只要快速找到第K个最大元素即可

解题方法

第K个最大元素，就是位置为 N-K 的元素 构造quickselect，这里就是检查我们使用partition函数找到的索引，如果我们的索引正好是 N-K，那么直接返回 如果不是继续在小区间里查找索引。整体时间复杂度是优于快排的O(nlogn)的

+ 时间复杂度:O(n)
+ 空间复杂度 O(logN) ： 划分函数的平均递归深度为 O(logN) 。



### [<font style="background-color:rgb(240, 240, 240);">前 K 个高频元素（347）</font>](https://leetcode.cn/problems/top-k-frequent-elements/)（堆）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和一个整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你返回其中出现频率前 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 高的元素。你可以按 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 返回答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
```

```python
import heapq

class Solution:
    def topKFrequent(self, nums, k):
        # 使用普通字典来统计每个数字出现的频率。
        frequencyMap = {}
        for num in nums:
            if num in frequencyMap:
                frequencyMap[num] += 1
            else:
                frequencyMap[num] = 1

        # 构建一个小顶堆，用于维护出现频率最高的k个数字。
        minHeap = []
        for num, freq in frequencyMap.items():
            # 如果堆还没满（即堆中元素少于k个），就直接添加当前元素
            if len(minHeap) < k:
                heapq.heappush(minHeap, (freq, num))
            # 如果堆已满，且当前元素的频率高于堆顶元素的频率，
            # 则替换堆顶元素（即频率最低的元素）。
            elif freq > minHeap[0][0]:
                heapq.heappushpop(minHeap, (freq, num))

        # 最后，从小顶堆中提取前k个频率最高的元素。
        topK = [num for freq, num in minHeap]
        return topK
```

时间复杂度：O(Nlogk)，其中 N 为数组的长度。我们首先遍历原数组，并使用哈希表记录出现次数，每个元素需要 O(1) 的时间，共需 O(N) 的时间。随后，我们遍历「出现次数数组」，由于堆的大小至多为 k，因此每次堆操作需要 O(logk) 的时间，共需 O(Nlogk) 的时间。二者之和为 O(Nlogk)。

空间复杂度：O(N)。哈希表的大小为 O(N)，而堆的大小为 O(k)，共计为 O(N)。



### [<font style="background-color:rgb(240, 240, 240);">多数元素(169)</font>](https://leetcode.cn/problems/majority-element/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个大小为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回其中的多数元素。多数元素是指在数组中出现次数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">大于</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">⌊ n/2 ⌋</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的元素。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以假设数组是非空的，并且给定的数组总是存在多数元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [3,2,3]
输出：3
```

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        #哈希表
        hashmap = dict()
        n = len(nums)
        for num in nums:
            if num in hashmap:
                hashmap[num] += 1
            else:
                hashmap[num] = 1
            
            if hashmap[num] > n//2:
                return num
        return None
```

时间复杂度：O(n)，其中 n 是数组 nums 的长度。我们遍历数组 nums 一次，对于 nums 中的每一个元素，将其插入哈希表都只需要常数时间。如果在遍历时没有维护最大值，在遍历结束后还需要对哈希表进行遍历，因为哈希表中占用的空间为 O(n)（可参考下文的空间复杂度分析），那么遍历的时间不会超过 O(n)。因此总时间复杂度为 O(n)。

空间复杂度：O(n)。



![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736414749859-6fde5f00-5ce2-47fa-9a1f-d9e98a896a76.png)

```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        nums.sort()
        return nums[len(nums) // 2]
```

时间复杂度：O(nlogn)。将数组排序的时间复杂度为 O(nlogn)。

空间复杂度：O(logn)。如果使用语言自带的排序算法，需要使用 O(logn) 的栈空间。如果自己编写堆排序，则只需要使用 O(1) 的额外空间。





### [<font style="background-color:rgb(240, 240, 240);">打家劫舍（198）</font>](https://leetcode.cn/problems/house-robber/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个代表每个房屋存放金额的非负整数数组，计算你</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 不触动警报装置的情况下 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，一夜之内能够偷窃到的最高金额。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。
```

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        #dp[i] 表示前 i 间房屋能偷窃到的最高总金额
        dp = [0 for i in range(n)]
        #初始化
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            #状态转移
            # 偷窃第 k 间房屋，那么就不能偷窃第 k−1 间房屋，偷窃总金额为前 k−2 间房屋的最高总金额与第 k 间房屋的金额之和。
            # 不偷窃第 k 间房屋，偷窃总金额为前 k−1 间房屋的最高总金额。
            # 在两个选项中选择偷窃总金额较大的选项，该选项对应的偷窃总金额即为前 k 间房屋能偷窃到的最高总金额。
            dp[i] = max(dp[i-2] + nums[i], dp[i-1])
        
        return dp[n-1]
```

时间复杂度：O(n)，其中 n 是数组长度。只需要对数组遍历一次。

空间复杂度：O(1)。使用滚动数组，可以只存储前两间房屋的最高总金额，而不需要存储整个数组的结果，因此空间复杂度是 O(1)。





### [<font style="background-color:rgb(240, 240, 240);">打家劫舍 III （337）</font>](https://leetcode.cn/problems/house-robber-iii/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">除了 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">两个直接相连的房子在同一天晚上被打劫</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，房屋将自动报警。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定二叉树的 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。返回 </font>_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在不触动警报的情况下</font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，小偷能够盗取的最高金额</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736765866368-142b3baa-9fad-49c2-bf16-7fc5fe8b9573.jpeg)

```plain
输入: root = [3,2,3,null,3,null,1]
输出: 7 
解释: 小偷一晚能够盗取的最高金额 3 + 3 + 1 = 7
```

```python
# 简化一下这个问题：一棵二叉树，树上的每个点都有对应的权值，每个点有两种状态（选中和不选中），问在不能同时选中有父子关系的点的情况下，能选中的点的最大权值和是多少。

# 我们可以用 f(o) 表示选择 o 节点的情况下，o 节点的子树上被选择的节点的最大权值和；g(o) 表示不选择 o 节点的情况下，o 节点的子树上被选择的节点的最大权值和；l 和 r 代表 o 的左右孩子。

# 当 o 不被选中时，o 的左右孩子可以被选中，也可以不被选中。对于 o 的某个具体的孩子 x，它对 o 的贡献是 x 被选中和不被选中情况下权值和的较大值。故 g(o)=max{f(l),g(l)}+max{f(r),g(r)}。
# 至此，我们可以用哈希表来存 f 和 g 的函数值，用深度优先搜索的办法后序遍历这棵二叉树，我们就可以得到每一个节点的 f 和 g。根节点的 f 和 g 的最大值就是我们要找的答案。

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> (int, int):
            if node is None:  # 递归边界
                return 0, 0  # 没有节点，怎么选都是 0
            l_rob, l_not_rob = dfs(node.left)  # 递归左子树
            r_rob, r_not_rob = dfs(node.right)  # 递归右子树
            rob = l_not_rob + r_not_rob + node.val  # 选
            not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob)  # 不选
            return rob, not_rob
        return max(dfs(root))  # 根节点选或不选的最大值
```

<font style="background-color:rgb(240, 240, 240);">我们可以看出，以上的算法对二叉树做了一次后序遍历，时间复杂度是 O(n)；</font>

<font style="background-color:rgb(240, 240, 240);">由于递归会使用到栈空间，空间代价是 O(n)，哈希表的空间代价也是 O(n)，故空间复杂度也是 O(n)。</font>

**<font style="background-color:rgb(240, 240, 240);"></font>**

**<font style="background-color:rgb(240, 240, 240);"></font>**

### [<font style="background-color:rgb(240, 240, 240);">除自身以外数组的乘积（238）</font>](https://leetcode.cn/problems/product-of-array-except-self/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回 数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">answer</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">answer[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 等于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中除 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 之外其余各元素的乘积 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">题目数据</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保证</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">之中任意元素的全部前缀元素和后缀的乘积都在 </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">32 位</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整数范围内。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不要使用除法，</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">且在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(n)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 时间复杂度内完成此题。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: nums = [1,2,3,4]
输出: [24,12,8,6]
```

方法一：左右乘积列表

我们不必将所有数字的乘积除以给定索引处的数字得到相应的答案，而是利用索引左侧所有数字的乘积和右侧所有数字的乘积（即前缀与后缀）相乘得到答案。

对于给定索引 i，我们将使用它左边所有数字的乘积乘以右边所有数字的乘积。下面让我们更加具体的描述这个算法。

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        L, R, res = [0]*n, [0]*n, [0]*n
        
        # L[i] 为索引 i 左侧所有元素的乘积
        # 对于索引为 '0' 的元素，因为左侧没有元素，所以 L[0] = 1
        L[0] = 1
        for i in range(1, n):
            L[i] = nums[i-1] * L[i-1]
        
        # R[i] 为索引 i 右侧所有元素的乘积
        # 对于索引为 'length-1' 的元素，因为右侧没有元素，所以 R[length-1] = 1
        R[n-1] = 1
        for i in range(n-2, -1, -1):
            R[i] = nums[i+1] * R[i+1]
        
        # 对于索引 i，除 nums[i] 之外其余各元素的乘积就是左侧所有元素的乘积乘以右侧所有元素的乘积
        for i in range(n):
            res[i] = L[i] * R[i]
        
        return res
```

时间复杂度：O(N)，其中 N 指的是数组 nums 的大小。预处理 L 和 R 数组以及最后的遍历计算都是 O(N) 的时间复杂度。

空间复杂度：O(N)，其中 N 指的是数组 nums 的大小。使用了 L 和 R 数组去构造答案，L 和 R 数组的长度为数组 nums 的大小。





### [<font style="background-color:rgb(240, 240, 240);">滑动窗口最大值（239）</font>](https://leetcode.cn/problems/sliding-window-maximum/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，有一个大小为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个数字。滑动窗口每次只向右移动一位。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">滑动窗口中的最大值 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
```

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        #对于「最大值」，我们可以想到一种非常合适的数据结构，那就是优先队列（堆），其中的大根堆可以帮助我们实时维护一系列元素中的最大值。
        # 注意 Python 默认的优先队列是小根堆
        
        #初始时，我们将数组 nums 的前 k 个元素放入优先队列中
        #为了方便判断堆顶元素与滑动窗口的位置关系，我们可以在优先队列中存储二元组 (num,index)，表示元素 num 在数组中的下标为 index。
        q = [(-nums[i], i) for i in range(k)]
        heapq.heapify(q)#将一个列表转换为堆：

        ans = [-q[0][0]]
        for i in range(k, n):
            #每当我们向右移动窗口时，我们就可以把一个新的元素放入优先队列中，此时堆顶的元素就是堆中所有元素的最大值。
            heapq.heappush(q, (-nums[i], i))#将元素添加到堆中：
            
            #然而这个最大值可能并不在滑动窗口中，在这种情况下，这个值在数组 nums 中的位置出现在滑动窗口左边界的左侧。
            #因此，当我们后续继续向右移动窗口时，这个值就永远不可能出现在滑动窗口中了，我们可以将其永久地从优先队列中移除。
            #我们不断地移除堆顶的元素，直到其确实出现在滑动窗口中
            #此时，堆顶元素就是滑动窗口中的最大值
            while q[0][1] <= i - k:  #堆顶元素的下标 <= i-k   说明堆顶元素在滑动窗内
                heapq.heappop(q)#从堆中弹出最小元素：
            ans.append(-q[0][0])#记录最大值：
        
        return ans
```

时间复杂度：O(nlogn)，其中 n 是数组 nums 的长度。在最坏情况下，数组 nums 中的元素单调递增，那么最终优先队列中包含了所有元素，没有元素被移除。由于将一个元素放入优先队列的时间复杂度为 O(logn)，因此总时间复杂度为 O(nlogn)。

空间复杂度：O(n)，即为优先队列需要使用的空间。这里所有的空间复杂度分析都不考虑返回的答案需要的 O(n) 空间，只计算额外的空间使用。





### [<font style="background-color:rgb(240, 240, 240);">移动零（283）</font>](https://leetcode.cn/problems/move-zeroes/)<font style="background-color:rgb(240, 240, 240);">（双指针）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，编写一个函数将所有</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">移动到数组的末尾，同时保持非零元素的相对顺序。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请注意</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，必须在不复制数组的情况下原地对数组进行操作。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">直接将非0的数字左移即可，再填充剩下的格子为0</font>

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        l, r = 0, 0
        #移动右指针
        while r < n:
            #当前元素不为0，则放到左指针处，同时左指针右移
            if nums[r] != 0:
                nums[l] = nums[r]
                #左指针右移
                l += 1
            r += 1
        
        #左指针右边全部置为0
        for i in range(l, n):
            nums[i] = 0
        
        return nums
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为序列长度。每个位置至多被遍历两次。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。只需要常数的空间存放若干变量。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [寻找重复数（287）](https://leetcode.cn/problems/find-the-duplicate-number/)（双指针）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个包含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n + 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个整数的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其数字都在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1, n]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 范围内（包括</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">），可知至少存在一个重复的整数。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">假设</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">只有</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一个重复的整数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">这个重复的数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你设计的解决方案必须 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不修改</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 且只用常量级 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(1)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的额外空间。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,3,4,2,2]
输出：2
```

```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        #对 nums 数组建图，每个位置 i 连一条 i→nums[i] 的边
        #由于存在的重复的数字 target，因此 target 这个位置一定有起码两条指向它的边，因此整张图一定存在环
        #我们要找到的 target 就是这个环的入口，那么整个问题就等价于 142. 环形链表 II。
        
        #先设置慢指针 slow 和快指针 fast ，慢指针每次走一步，快指针每次走两步
        slow, fast = 0, 0
        
        #初始化
        slow = nums[slow]
        fast = nums[nums[fast]]
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]
        
        #两个指针在有环的情况下一定会相遇，此时我们再将 slow 放置起点 0，两个指针每次同时移动一步，相遇的点就是答案。
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        
        return slow
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。「Floyd 判圈算法」时间复杂度为线性的时间复杂度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。我们只需要常数空间存放若干变量。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">戳气球（312）</font>](https://leetcode.cn/problems/burst-balloons/)<font style="background-color:rgb(240, 240, 240);">（DFS）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">有</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个气球，编号为</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">到</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n - 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，每个气球上都标有一个数字，这些数字存在数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">现在要求你戳破所有的气球。戳破第</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个气球，你可以获得 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums[i - 1] * nums[i] * nums[i + 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">枚硬币。 这里的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i - 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i + 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">代表和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 相邻的两个气球的序号。如果</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i - 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">或</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i + 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">超出了数组的边界，那么就当它是一个数字为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的气球。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">求所能获得硬币的最大数量。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [3,1,5,8]
输出：167
解释：
nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
coins =  3*1*5    +   3*5*8   +  1*3*8  + 1*8*1 = 167
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736754472820-0f14f35e-9025-41e1-b3c6-59430d4c6ed4.png)

```python
class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        #我们观察戳气球的操作，发现这会导致两个气球从不相邻变成相邻，使得后续操作难以处理。于是我们倒过来看这些操作，将全过程看作是每次添加一个气球。
        n = len(nums)
        val = [1] + nums + [1]

        #我们定义方法 solve，令 solve(i,j) 表示将开区间 (i,j) 内的位置全部填满气球能够得到的最多硬币数
        #由于是开区间，因此区间两端的气球的编号就是 i 和 j，对应着 val[i] 和 val[j]。
        @lru_cache(None)#为了防止重复计算，我们存储 solve 的结果，使用记忆化搜索的方法优化时间复杂度。
        def solve(left: int, right: int) -> int:
            #当 i≥j−1 时，开区间中没有气球，solve(i,j) 的值为 0；
            if left >= right - 1:
                return 0
            #当 i<j−1 时，我们枚举开区间 (i,j) 内的全部位置 mid，令 mid 为当前区间第一个添加的气球，该操作能得到的硬币数为 val[i]×val[mid]×val[j]
            best = 0
            #同时我们递归地计算分割出的两区间对 solve(i,j) 的贡献，这三项之和的最大值，即为 solve(i,j) 的值。
            for i in range(left + 1, right):
                total = val[left] * val[i] * val[right]
                total += solve(left, i) + solve(i, right)
                best = max(best, total)

            return best

        return solve(0, n + 1)
```



### [零钱兑换（322）](https://leetcode.cn/problems/coin-change/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">coins</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示不同面额的硬币；以及一个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">amount</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示总金额。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">计算并返回可以凑成总金额所需的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最少的硬币个数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果没有任何一种硬币组合能组成总金额，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以认为每种硬币的数量是无限的。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：coins = [1, 2, 5], amount = 11
输出：3 
解释：11 = 5 + 5 + 1
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736759280042-49075cd4-8d5d-4d41-ae50-114c322143ef.png)

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        #定义 dp[i] 为组成金额 i 所需最少的硬币数量
        dp[0] = 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                #F(i)=min j=0…n−1 F(i−cj​)+1
                #其中 cj  代表的是第 j 枚硬币的面值，即我们枚举最后一枚硬币面额是 cj ，那么需要从 i−cj这个金额的状态 F(i−cj)转移过来，再算上枚举的这枚硬币数量 1 的贡献，由于要硬币数量最少，所以 F(i) 为前面能转移过来的状态的最小值加上枚举的硬币数量 1 。
                dp[x] = min(dp[x], dp[x - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1 
```

时间复杂度：O(Sn)，其中 S 是金额，n 是面额数。我们一共需要计算 O(S) 个状态，S 为题目所给的总金额。对于每个状态，每次需要枚举 n 个面额来转移状态，所以一共需要 O(Sn) 的时间复杂度。

空间复杂度：O(S)。数组 dp 需要开长度为总金额 S 的空间。



### [零钱兑换 II (518)](https://leetcode.cn/problems/coin-change-ii/description/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">coins</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示不同面额的硬币，另给一个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">amount</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示总金额。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你计算并返回可以凑成总金额的硬币组合数。如果任何硬币组合都无法凑出总金额，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">假设每一种面额的硬币有无限个。 </font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">题目数据保证结果符合 32 位带符号整数。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：amount = 5, coins = [1, 2, 5]
输出：4
解释：有四种方式可以凑成总金额：
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：amount = 3, coins = [2]
输出：0
解释：只用面额 2 的硬币不能凑成总金额 3 。
```

```python
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [0] * (amount + 1)    # dp[i]表示凑成金额i的组合数，初始都为0表示不可凑
        # 我们可以定义 dp[a] 表示凑成金额 a 的组合数。 那么当我们使用面值为 c 的硬币来构成金额 a 时，其状态取决于 a - c，即状态转移方程为：dp[a] = ∑dp[a-c]。
        dp[0] = 1      # 金额0有一种组合方式，由0枚硬币组成
        # 枚举每一种硬币
        for c in coins:
            # 枚举每一个金额
            for a in range(c, amount + 1):
                dp[a] += dp[a - c]     # 当使用面额为c的硬币时，a的状态取决于a-c

        return dp[amount] 

```

### [<font style="background-color:rgb(240, 240, 240);">找到所有数组中消失的数字（448）</font>](https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个整数的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 在区间 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1, n]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 内。请你找出所有在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1, n]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 范围内但没有出现在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中的数字，并以数组的形式返回结果。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [4,3,2,7,8,2,3,1]
输出：[5,6]
```

```python
class Solution(object):
    def findDisappearedNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        for i, num in enumerate(nums):
            #如果 第 nums[i]−1 位置的元素已经是负数了，表示 nums[i] 已经出现过了，就不用再把第 nums[i]−1 位置的元素乘以 -1
            if nums[abs(num) - 1] > 0:
                #当前元素是 nums[i]，那么我们把第 nums[i]−1 位置的元素 乘以 -1，表示这个该位置出现过。
                nums[abs(num) - 1] *= -1
        res = []
        #对数组中的每个位置遍历一遍，如果 i 位置的数字是正数，说明 i 未出现过。
        for i in range(len(nums)):
            if nums[i] > 0:
                res.append(i + 1)
        return res
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，用时 348ms，击败了 53.91% 的用户；</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，空间 20.1M，击败了 81.40% 的用户。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">目标和（494）</font>](https://leetcode.cn/problems/target-sum/)<font style="background-color:rgb(240, 240, 240);">（DFS）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个非负整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">向数组中的每个整数前添加 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'+'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">或</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'-'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，然后串联起所有整数，可以构造一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表达式</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums = [2, 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，可以在</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">之前添加</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'+'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，在</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">之前添加</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'-'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，然后串联起来得到表达式</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">"+2-1"</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回可以通过上述方法构造的、运算结果等于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的不同 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表达式</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的数目。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,1,1,1,1], target = 3
输出：5
解释：一共有 5 种方法让最终目标和为 3 。
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736837795058-12d51086-9d2c-4b00-bdad-3fbee55f0383.png)

```python
class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        s = sum(nums) - abs(target)
        if s < 0 or s % 2:
            return 0
        m = s // 2  # 背包容量

        @cache  # 缓存装饰器，避免重复计算 dfs 的结果（记忆化）
        def dfs(i: int, c: int) -> int:
            if i < 0:
                return 1 if c == 0 else 0
            if c < nums[i]:
                return dfs(i - 1, c)  # 只能不选
            #加法原理，如果事件 A 和事件 B 是互斥的（即不能同时发生，不选 nums[i] 的同时，又选了 nums[i]），那么发生事件 A 或事件 B 的总数等于事件 A 的数量加上事件 B 的数量
            return dfs(i - 1, c) + dfs(i - 1, c - nums[i])  # 不选 + 选
        return dfs(len(nums) - 1, m)


```

时间复杂度：O(nm)，其中 n 为 nums 的长度，m 为 nums 的元素和减去 target 的绝对值。由于每个状态只会计算一次，动态规划的时间复杂度 = 状态个数 × 单个状态的计算时间。本题状态个数等于 O(nm)，单个状态的计算时间为 O(1)，所以动态规划的时间复杂度为 O(nm)。

空间复杂度：O(nm)。保存多少状态，就需要多少空间。





### [<font style="background-color:rgb(240, 240, 240);">每日温度（739）</font>](https://leetcode.cn/problems/daily-temperatures/)（单调栈）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">temperatures</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，表示每天的温度，返回一个数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">answer</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">answer[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是指对于第 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 来代替。</font>

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        res = [0] * n
        for i in range(n-1):
            for j in range(i+1, n):
                if temperatures[j] > temperatures[i]:
                    res[i] = j-i
                    break
        return res
```

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        length = len(temperatures)
        ans = [0] * length
        #维护一个存储下标的单调栈，从栈底到栈顶的下标对应的温度列表中的温度依次递减
        stack = []
        for i in range(length):
            temperature = temperatures[i]
            #如果栈为空，则直接将 i 进栈
            #如果栈不为空，则比较栈顶元素 prevIndex 对应的温度 temperatures[prevIndex] 和当前温度 temperatures[i]，如果 temperatures[i] > temperatures[prevIndex]，则将 prevIndex 移除，并将 prevIndex 对应的等待天数赋为 i - prevIndex，重复上述操作直到栈为空或者栈顶元素对应的温度小于等于当前温度，然后将 i 进栈。
            while stack and temperature > temperatures[stack[-1]]:
                prev_index = stack.pop()
                ans[prev_index] = i - prev_index
            stack.append(i)
        #由于单调栈满足从栈底到栈顶元素对应的温度递减，因此每次有元素进栈时，会将温度更低的元素全部移除，并更新出栈元素对应的等待天数，这样可以确保等待天数一定是最小的。

        return ans
```

时间复杂度：O(n)，其中 n 是温度列表的长度。正向遍历温度列表一遍，对于温度列表中的每个下标，最多有一次进栈和出栈的操作。

空间复杂度：O(n)，其中 n 是温度列表的长度。需要维护一个单调栈存储温度列表中的下标。





### [<font style="background-color:rgb(240, 240, 240);">除法求值（399）</font>](https://leetcode.cn/problems/evaluate-division/)<font style="background-color:rgb(240, 240, 240);">（DFS）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个变量对数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">equations</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个实数值数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">values</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">作为已知条件，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">equations[i] = [A</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">, B</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">values[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">共同表示等式</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">A</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> / B</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> = values[i]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。每个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">A</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">或</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">B</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是一个表示单个变量的字符串。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">另有一些以数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">queries</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示的问题，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">queries[j] = [C</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">, D</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示第</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个问题，请你根据已知条件找出</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> / D</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> = ?</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的结果作为答案。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">所有问题的答案</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果存在某个无法确定的答案，则用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1.0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">替代这个答案。如果问题中出现了给定的已知条件中没有出现的字符串，也需要用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1.0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">替代这个答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">输入总是有效的。你可以假设除法运算中不会出现除数为 0 的情况，且不存在任何矛盾的结果。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">未在等式列表中出现的变量是未定义的，因此无法确定它们的答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
输出：[6.00000,0.50000,-1.00000,1.00000,-1.00000]
解释：
条件：a / b = 2.0, b / c = 3.0
问题：a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ?
结果：[6.0, 0.5, -1.0, 1.0, -1.0 ]
注意：x 是未定义的 => -1.0
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736823228647-29fbe096-d541-45c7-9009-dd6da7e39040.png)

```python
class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        """建图部分"""
        g = defaultdict(list)
        for (e1,e2),v in zip(equations,values):
            g[e1].append([e2,v])
            g[e2].append([e1,1 / v])
        lst = []#存放最后结果
        def dfs(cur: str,end:str,tot: float) -> bool:
            if cur == end:
                nonlocal res 
                res = tot
                return True
            vis.add(cur)
            for nxt,v in g[cur]:
                if nxt not in vis:
                    # 剪枝
                    if dfs(nxt,end,tot * v):
                        return True 
            return False
            
        for start,end in queries:
            vis = set()
            res = -1.0
            if start in g and end in g:
                dfs(start,end,1)
            lst.append(res)
        return lst
```

时间复杂度：O(ML+Q⋅(L+M))，其中 M 为边的数量，Q 为询问的数量，L 为字符串的平均长度。构建图时，需要处理 M 条边，每条边都涉及到 O(L) 的字符串比较；处理查询时，每次查询首先要进行一次 O(L) 的比较，然后至多遍历 O(M) 条边。

空间复杂度：O(NL+M)，其中 N 为点的数量，M 为边的数量，L 为字符串的平均长度。为了将每个字符串映射到整数，需要开辟空间为 O(NL) 的哈希表；随后，需要花费 O(M) 的空间存储每条边的权重；处理查询时，还需要 O(N) 的空间维护访问队列。最终，总的复杂度为 O(NL+M+N)=O(NL+M)。



## 1.2 子数组和
### 两数之和
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和一个整数目标值 </font>`<font style="color:rgba(38, 38, 38, 0.75);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你在该数组中找出 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和为目标值 </font>**`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>_`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">  的那 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">两个</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 整数，并返回它们的数组下标。</font>

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashtable = dict()
        for i, num in enumerate(nums):
            if target - num in hashtable:
                return [hashtable[target - num], i]
            hashtable[nums[i]] = i
        return []

```

时间复杂度：O(N)，其中 N 是数组中的元素数量。对于每一个元素 x，我们可以 O(1) 地寻找 target - x。

空间复杂度：O(N)，其中 N 是数组中的元素数量。主要为哈希表的开销。





### 三数之和
[https://leetcode.cn/problems/3sum/description/](https://leetcode.cn/problems/3sum/description/)

排序+双指针

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，判断是否存在三元组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[nums[i], nums[j], nums[k]]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 满足 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i != j</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i != k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 且 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j != k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，同时还满足 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums[i] + nums[j] + nums[k] == 0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。请你返回所有和为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 且不重复的三元组。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">这个方法就是我们常说的「双指针」，当我们需要枚举数组中的两个元素时，如果我们发现随着第一个元素的递增，第二个元素是递减的，那么就可以使用双指针的方法</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，判断是否存在三元组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[nums[i], nums[j], nums[k]]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">满足</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i != j</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i != k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">且</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j != k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，同时还满足</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums[i] + nums[j] + nums[k] == 0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。请你返回所有和为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">且不重复的三元组。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">答案中不可以包含重复的三元组。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
```

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        k = 0
        for k in range(0, len(nums) - 2):
            if nums[k] > 0 :break #排序后，nums[k]需要<0，才可能有：nums[k] + nums[i] + nums[j] = 0
            if k>0 and nums[k] == nums[k-1] : continue #跳过重复的元素
            i, j = k+1, len(nums)-1
            #双指针
            while i < j :
                s = nums[k] + nums[i] + nums[j]
                #和<0 左指针右移
                if s < 0:
                    i += 1
                    while i < j and nums[i-1] == nums[i] : i += 1 #跳过重复元素
                #和>0 右指针左移
                elif s > 0:
                    j -= 1
                    while i < j and nums[j+1] == nums[j] : j -= 1 #跳过重复元素
                else:
                    res.append([nums[k], nums[i], nums[j]])
                    i += 1
                    j -= 1
                    while i < j and nums[i-1] == nums[i] : i += 1
                    while i < j and nums[j+1] == nums[j] : j -= 1
        return res


```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：其中固定指针</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">循环复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，双指针</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：指针使用常数大小的额外空间。</font>



### 最接近的三数之和
[https://leetcode.cn/problems/3sum-closest/description/](https://leetcode.cn/problems/3sum-closest/description/)

排序+双指针

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个长度为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和 一个目标值 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。请你从</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中选出三个整数，使它们的和与 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 最接近。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回这三个数的和。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">假定每组输入只存在恰好一个解。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [-1,2,1,-4], target = 1
输出：2
解释：与 target 最接近的和是 2 (-1 + 2 + 1 = 2)。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [0,0,0], target = 1
输出：0
解释：与 target 最接近的和是 0（0 + 0 + 0 = 0）。
```

```python
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        res = inf
        k = 0
        for k in range(0, len(nums) - 2):
            if k>0 and nums[k] == nums[k-1] : continue #跳过重复的元素
            i, j = k+1, len(nums)-1
            #双指针
            while i < j :
                s = nums[k] + nums[i] + nums[j]
                res = res if abs(target-s) > abs(target-res) else s
                #和<target 左指针右移
                if s < target:
                    i += 1
                    while i < j and nums[i-1] == nums[i] : i += 1 #跳过重复元素
                #和>0 右指针左移
                elif s > target:
                    j -= 1
                    while i < j and nums[j+1] == nums[j] : j -= 1 #跳过重复元素
                else:
                    res = s
                    break
        return res
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：其中固定指针</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">循环复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，双指针</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">j</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：指针使用常数大小的额外空间。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### 四数之和
双指针

[https://leetcode.cn/problems/4sum/description/](https://leetcode.cn/problems/4sum/description/)

思路和 15. 三数之和 一样，排序后，枚举 nums[a] 作为第一个数，枚举 nums[b] 作为第二个数，那么问题变成找到另外两个数，使得这四个数的和等于 target，这可以用双指针解决。

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res = []
        k = 0
        #枚举第一个数
        for l in range(0, len(nums) - 3):
            if l>0 and nums[l] == nums[l-1] : continue #跳过重复的元素
            #枚举第二个数
            for k in range(l+1, len(nums) - 2):
                if k>l+1 and nums[k] == nums[k-1] : continue #跳过重复的元素

                # 剩下两数采用双指针
                i, j = k+1, len(nums)-1
                #双指针
                while i < j :
                    s = nums[l] + nums[k] + nums[i] + nums[j]
                    #和<0 左指针右移
                    if s < target:
                        i += 1
                        while i < j and nums[i-1] == nums[i] : i += 1 #跳过重复元素
                    #和>0 右指针左移
                    elif s > target:
                        j -= 1
                        while i < j and nums[j+1] == nums[j] : j -= 1 #跳过重复元素
                    else:
                        res.append([nums[l], nums[k], nums[i], nums[j]])
                        i += 1
                        j -= 1
                        while i < j and nums[i-1] == nums[i] : i += 1
                        while i < j and nums[j+1] == nums[j] : j -= 1
        return res
```

时间复杂度：O(n 3)，其中 n 为 nums 的长度。排序 O(nlogn)。两重循环枚举第一个数和第二个数，然后 O(n) 双指针枚举第三个数和第四个数。所以总的时间复杂度为 O(n 3 )。

空间复杂度：O(1)。忽略返回值和排序的栈开销，仅用到若干变量。



### [组合总和](https://leetcode.cn/problems/combination-sum/)
回溯 DFS

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">无重复元素</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个目标整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，找出 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中可以使数字和为目标数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的 所有</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不同组合</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，并以列表形式返回。你可以按</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回这些组合。</font>

`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">同一个</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数字可以</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">无限制重复被选取</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果至少一个数字的被选数量不同，则两种组合是不同的。 </font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于给定的输入，保证和为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的不同组合数少于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">150</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于这类寻找所有可行解的题，我们都可以尝试用「搜索回溯」的方法来解决。</font>

```plain
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于这类寻找所有可行解的题，我们都可以尝试用「搜索回溯」的方法来解决。</font>

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        
        def dfs(target, idx):
            #走到最后一个数字
            if idx == len(candidates):
                return
            #找到目标结果
            if target == 0:
                ans.append(combine.copy()) #copy() 
                return
            #分叉1 直接跳过
            dfs(target, idx+1)
            #分叉2 选择当前数字
            if (target - candidates[idx] >= 0):
                combine.append(candidates[idx])
                dfs(target-candidates[idx],idx)
                combine.pop()

        ans = []
        combine = []
        dfs(target, 0)
        return ans
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1735819150572-b8734bf2-9b15-4b77-afcc-6ecc2ee0aae6.png)





### [最大子数组和](https://leetcode.cn/problems/maximum-subarray/)
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。</font>

**<font style="background-color:rgb(240, 240, 240);">子数组</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是数组中的一个连续部分。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [1]
输出：1
```

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        res = -inf
        pre = 0
        for i in range(n):
            # f(i)=max{f(i−1)+nums[i],nums[i]}
            # f(i)表示以nums[i]结尾的最大连续子串和
            #考虑到 f(i) 只和 f(i−1) 相关，于是我们可以只用一个变量 pre 来维护对于当前 f(i) 的 f(i−1) 的值是多少，从而让空间复杂度降低到 O(1)，这有点类似「滚动数组」的思想。
            pre = max(pre + nums[i], nums[i])
            res = max(pre, res)
        return res
```

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        max_sum = dp[0]

        for i in range(1, n):
            dp[i] = max(nums[i], dp[i-1] + nums[i])
            max_sum = max(max_sum, dp[i])

        return max_sum
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数组的长度。我们只需要遍历一遍数组即可求得答案。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。我们只需要常数空间存放若干变量。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">和为 K 的子数组（560）</font>](https://leetcode.cn/problems/subarray-sum-equals-k/)（前缀和+哈希表）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你统计并返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">该数组中和为 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>_`_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的子数组的个数 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">子数组是数组中元素的连续非空序列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,1,1], k = 2
输出：2
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736847716232-f2c9f112-e463-4467-9187-dda8f4246978.png)

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        pre = 0
        n = len(nums)
        #建立哈希表，以和为键，出现次数为对应的值，记录 pre[i] 出现的次数
        hashmap = dict()
        hashmap[0] = 1
        for i in range(n):
            #前缀和
            pre += nums[i]
            #统计有多少个前缀和为 pre[i]−k 的 pre[j] (以 i 结尾的和为 k 的连续子数组个数)
            if pre-k in hashmap:
                count += hashmap[pre-k]

            #pre加入hash表
            if pre in hashmap:
                hashmap[pre] += 1
            else:
                hashmap[pre] = 1
        return count
```

时间复杂度：O(n)，其中 n 为数组的长度。我们遍历数组的时间复杂度为 O(n)，中间利用哈希表查询删除的复杂度均为 O(1)，因此总时间复杂度为 O(n)。

空间复杂度：O(n)，其中 n 为数组的长度。哈希表在最坏情况下可能有 n 个不同的键值，因此需要 O(n) 的空间复杂度。

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        res = 0
        #统计以i结尾的和为k的子数组数量
        for i in range(n):
            #子数组下标：[j:i]
            sum = 0
            for j in range(i, -1, -1):
                sum += nums[j]
                if sum == k:
                    res += 1
        return res
```

时间复杂度：O(n^2 )，其中 n 为数组的长度。枚举子数组开头和结尾需要 O(n ^2 ) 的时间，其中求和需要 O(1) 的时间复杂度，因此总时间复杂度为 O(n ^2 )。

空间复杂度：O(1)。只需要常数空间存放若干变量。



## 1.3 排列
### **全排列1 （无重复数字）**
回溯/DFS

[https://leetcode.cn/problems/permutations/description/](https://leetcode.cn/problems/permutations/description/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个不含重复数字的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回其 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">所有可能的全排列</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。你可以 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">按任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 返回答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        
        def dfs(depth):
            #找到目标结果
            if depth == n:
                ans.append(combine.copy()) #copy() 
                return
            #剩余可选数字集合
            doc_nums = [i for i in nums if i not in combine]
            for num in doc_nums:
                #排列中加入该数字
                combine.append(num)
                #深度+1
                dfs(depth+1)
                #回溯
                combine.pop()

        n = len(nums)
        ans = []
        combine = []
        dfs(0)
        return ans
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736230654828-f0565bce-4e8a-489e-98f8-0bd9de8003ab.png)

### [**全排列 II**](https://leetcode.cn/problems/permutations-ii/)**（有重复数字）**
回溯/DFS

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个可包含重复数字的序列 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，</font>_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">按任意顺序</font>**_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 返回所有不重复的全排列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]
```

```python
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        def dfs(depth):
            #找到目标结果
            if depth == n:
                #非重复结果
                if combine not in ans:
                    ans.append(combine.copy()) #copy() 
                return
            #剩余可选数字集合
            doc_nums = nums.copy()
            for num in combine:
                doc_nums.remove(num)

            for num in doc_nums:
                #排列中加入该数字
                combine.append(num)
                #深度+1
                dfs(depth+1)
                #回溯
                combine.pop()

        n = len(nums)
        ans = []
        combine = []
        dfs(0)
        return ans
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736230651410-266be7b5-ee54-4bc1-9cf1-545e20fe954a.png)

### [下一个排列](https://leetcode.cn/problems/next-permutation/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整数数组的一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">排列</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">  就是将其所有成员以序列或线性顺序排列。</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">arr = [1,2,3]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，以下这些都可以视作</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">arr</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的排列：</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1,2,3]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1,3,2]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[3,1,2]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[2,3,1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整数数组的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">下一个排列</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是指其整数的下一个字典序更大的排列。更正式地，如果数组的所有排列根据其字典顺序从小到大排列在一个容器中，那么数组的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">下一个排列</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">就是在这个有序容器中排在它后面的那个排列。如果不存在下一个更大的排列，那么这个数组必须重排为字典序最小的排列（即，其元素按升序排列）。</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">arr = [1,2,3]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的下一个排列是</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1,3,2]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">类似地，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">arr = [2,3,1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的下一个排列是</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[3,1,2]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">而</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">arr = [3,2,1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的下一个排列是</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[1,2,3]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，因为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[3,2,1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不存在一个字典序更大的排列。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找出</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的下一个排列。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">必须</font>[**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">原地</font>**](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">修改，只允许使用额外常数空间。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,2,3]
输出：[1,3,2]
```



![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1735816685309-e76b432f-3a16-45dd-bd6f-6ae6b72db4aa.png)

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        i = len(nums) - 2
        #从右往左开始找，让这个「较小数」尽量靠右。首先从后向前查找第一个顺序对 (i,i+1)，满足 a[i]<a[i+1]。这样「较小数」即为 a[i]。此时 [i+1,n) 必然是下降序列。
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        #如果找到了顺序对，那么在区间 [i+1,n) 中从后向前查找第一个元素 j 满足 a[i]<a[j]。这样「较大数」即为 a[j]。
        if i >= 0:
            j = len(nums) - 1
            while j >= 0 and nums[i] >= nums[j]:
                j -= 1
            #交换 a[i] 与 a[j]
            nums[i], nums[j] = nums[j], nums[i]
        
        #此时可以证明区间 [i+1,n) 必为降序。我们可以直接使用双指针反转区间 [i+1,n) 使其变为升序，而无需对该区间进行排序。
        left, right = i + 1, len(nums) - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为给定序列的长度。我们至多只需要扫描两次序列，以及进行一次反转操作。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">，只需要常数的空间存放若干变量。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

## <font style="background-color:rgb(240, 240, 240);">1.4 二维数组</font>
### 二维数组dfs思路
```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(grid, r, c):
            #判断边界
            if not in_area(grid, r, c):
                return 
            
            #判断是否岛屿
            if grid[r][c] != 1:
                return 

            #已经遍历过的地方，标记为大海
            grid[r][c] = 2
            
            #访问上下左右四个相邻点
            dfs(grid, r-1, c)
            dfs(grid, r+1, c)
            dfs(grid, r, c-1)
            dfs(grid, r, c+1)
        
        def in_area(grid, r, c):
            return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])
```

### [旋转图像](https://leetcode.cn/problems/rotate-image/)
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736134094315-acb0204a-566d-498b-8037-c2da14a94e22.png)

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)
        tmp_matrix = copy.deepcopy(matrix)
        for i in range(n):
            for j in range(n):
                matrix[j][n-1-i] = tmp_matrix[i][j]
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如以上代码所示，遍历矩阵所有元素的时间复杂度为 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；由于借助了一个辅助矩阵，</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">为 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736134128246-3bf6db10-ca77-4793-91b5-e2310a991332.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736134152008-4ae06abc-8ebf-4e25-98ff-d538cfaff138.png)

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        n = len(matrix)
        for i in range(n // 2):
            for j in range((n + 1) // 2):
                #暂存A
                tmp = matrix[i][j]
                #D->A
                matrix[i][j] = matrix[n - 1 - j][i]
                #C->D
                matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
                #B->C
                matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
                #A->b
                matrix[j][n - 1 - i] = tmp


```

时间复杂度 O(N 2 ) ： 其中 N 为输入矩阵的行（列）数。需要将矩阵中每个元素旋转到新的位置，即对矩阵所有元素操作一次，使用 O(N 2) 时间。

空间复杂度 O(1) ： 临时变量 tmp 使用常数大小的额外空间。值得注意，当循环中进入下轮迭代，上轮迭代初始化的 tmp 占用的内存就会被自动释放，因此无累计使用空间。



### [<font style="background-color:rgb(240, 240, 240);">合并区间</font>](https://leetcode.cn/problems/merge-intervals/)
排序

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">以数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">intervals</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 表示若干个区间的集合，其中单个区间为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">intervals[i] = [start</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">, end</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。请你合并所有重叠的区间，并返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
```

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        #首先，我们将列表中的区间按照左端点升序排序。
        intervals.sort(key=lambda x: x[0])
        # 然后我们将第一个区间加入 merged 数组中，并按顺序依次考虑之后的每个区间：
        merged = [intervals[0]]
        for interval in intervals[1:]:
            # 如果当前区间的左端点在数组 merged 中最后一个区间的右端点之后，那么它们不会重合，我们可以直接将这个区间加入数组 merged 的末尾；
            if interval[0] > merged[-1][1]:
                merged.append(interval)
            # 否则，它们重合，我们需要用当前区间的右端点更新数组 merged 中最后一个区间的右端点，将其置为二者的较大值。
            else:
                merged[-1][1] = max(interval[1], merged[-1][1])
        return merged
```

时间复杂度：O(nlogn)，其中 n 为区间的数量。除去排序的开销，我们只需要一次线性扫描，所以主要的时间开销是排序的 O(nlogn)。

空间复杂度：O(logn)，其中 n 为区间的数量。这里计算的是存储答案之外，使用的额外空间。O(logn) 即为排序所需要的空间复杂度。





### [螺旋矩阵(54)](https://leetcode.cn/problems/spiral-matrix/description/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 行 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 列的矩阵 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">matrix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请按照 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">顺时针螺旋顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回矩阵中的所有元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1740930169482-488e6b34-73eb-482e-90c4-76898ed8eeb7.jpeg)

```plain
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

1. 空值处理： 当 matrix 为空时，直接返回空列表 [] 即可。
2. 初始化： 矩阵 左、右、上、下 四个边界 l , r , t , b ，用于打印的结果列表 res 。
3. 循环打印： “从左向右、从上向下、从右向左、从下向上” 四个方向循环打印。
    - 根据边界打印，即将元素按顺序添加至列表 res 尾部。
    - 边界向内收缩 1 （代表已被打印）。
    - 判断边界是否相遇（是否打印完毕），若打印完毕则跳出。
4. 返回值： 返回 res 即可。

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix: return []
        l, r, t, b, res = 0, len(matrix[0]) - 1, 0, len(matrix) - 1, []
        while True:
            for i in range(l, r + 1): res.append(matrix[t][i]) # left to right
            t += 1
            if t > b: break
            for i in range(t, b + 1): res.append(matrix[i][r]) # top to bottom
            r -= 1
            if l > r: break
            for i in range(r, l - 1, -1): res.append(matrix[b][i]) # right to left
            b -= 1
            if t > b: break
            for i in range(b, t - 1, -1): res.append(matrix[i][l]) # bottom to top
            l += 1
            if l > r: break
        return res
```

+ **<font style="background-color:rgb(240, 240, 240);">时间复杂度</font>****<font style="background-color:rgb(240, 240, 240);"> </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MN</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>****<font style="background-color:rgb(240, 240, 240);"> </font>****<font style="background-color:rgb(240, 240, 240);">：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">M</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">,</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">分别为矩阵行数和列数。</font>
+ **<font style="background-color:rgb(240, 240, 240);">空间复杂度 </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font>****<font style="background-color:rgb(240, 240, 240);"> ：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 四个边界 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">l</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> , </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">r</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> , </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> , </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">b</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 使用常数大小的额外空间。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [螺旋矩阵2(59)](https://leetcode.cn/problems/spiral-matrix-ii/description/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个正整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，生成一个包含</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font><sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font></sup>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 所有元素，且元素按顺时针顺序螺旋排列的 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n x n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">正方形矩阵</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">matrix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1740930300735-1f35ce49-2152-4262-a345-5daa745a1306.jpeg)

```plain
输入：n = 3
输出：[[1,2,3],[8,9,4],[7,6,5]]
```

初始化一个 n×n 大小的矩阵 mat，然后模拟整个向内环绕的填入过程：

1. 定义当前左右上下边界 l,r,t,b，初始值 num = 1，迭代终止值 tar = n * n；
2. 当 num <= tar 时，始终按照 从左到右 从上到下 从右到左 从下到上 填入顺序循环，每次填入后：
    - **执行 num += 1**：得到下一个需要填入的数字；
    - **更新边界**：例如从左到右填完后，上边界 t += 1，相当于上边界向内缩 1。
3. 使用num <= tar而不是l < r || t < b作为迭代条件，是为了解决当n为奇数时，矩阵中心数字无法在迭代过程中被填充的问题。
4. 最终返回 mat 即可。

```python
class Solution:
    def generateMatrix(self, n: int) -> [[int]]:
        l, r, t, b = 0, n - 1, 0, n - 1
        mat = [[0 for _ in range(n)] for _ in range(n)]
        num, tar = 1, n * n
        while num <= tar:
            for i in range(l, r + 1): # left to right
                mat[t][i] = num
                num += 1
            t += 1
            for i in range(t, b + 1): # top to bottom
                mat[i][r] = num
                num += 1
            r -= 1
            for i in range(r, l - 1, -1): # right to left
                mat[b][i] = num
                num += 1
            b -= 1
            for i in range(b, t - 1, -1): # bottom to top
                mat[i][l] = num
                num += 1
            l += 1
        return mat

```

时间复杂度：O(n<sup>2</sup>)，其中 n 是给定的正整数。矩阵的大小是 n×n，需要填入矩阵中的每个元素。

空间复杂度：O(1)。除了返回的矩阵以外，空间复杂度是常数。





### [<font style="background-color:rgb(240, 240, 240);">不同路径(62)</font>](https://leetcode.cn/problems/unique-paths/)
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一个机器人位于一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m x n</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">网格的左上角 （起始点在下图中标记为 “Start” ）。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">问总共有多少条不同的路径？</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736162979708-b7b003a0-52fa-4995-bef1-3276f545df3a.png)

```plain
输入：m = 3, n = 7
输出：28
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下
```

```python
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1 for i in range(n)] for j in range(m)]
        for i in range(1,m):
            for j in range(1,n):
                #对于每一个点 (i, j)，到达这个点的方式只有从上一个点 (i - 1, j) 和左边的点 (i, j - 1)，所以 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]。
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m-1][n-1]
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∗</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∗</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>

<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">不同路径 II（63）</font>](https://leetcode.cn/problems/unique-paths-ii/)
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m x n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">grid</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。一个机器人初始位于</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">左上角</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（即</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">grid[0][0]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）。机器人尝试移动到</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">右下角</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（即</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">grid[m - 1][n - 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）。机器人每次只能向下或者向右移动一步。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">网格中的障碍物和空位置分别用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">来表示。机器人的移动路径中不能包含</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任何</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 有障碍物的方格。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回机器人能够到达右下角的不同路径数量。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">测试用例保证答案小于等于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2 * 10</font><sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">9</font></sup>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736166239954-ea9619dd-61e7-4122-aa47-7a62da4e1fbe.jpeg)

```plain
输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
输出：2
解释：3x3 网格的正中间有一个障碍物。
从左上角到右下角一共有 2 条不同的路径：
1. 向右 -> 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右 -> 向右
```

```python
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])
        dp = [[1]*n for j in range(m)]
        #初始化第一行
        flag = 0
        for i in range(n):
            if obstacleGrid[0][i] == 1:
                flag = 1
            if flag == 1:
                dp[0][i] = 0
        #初始化第一列
        flag = 0
        for i in range(m):
            if obstacleGrid[i][0] == 1:
                flag = 1
            if flag == 1:
                dp[i][0] = 0
        # return dp
        for i in range(1,m):
            for j in range(1,n):
                if obstacleGrid[i][j] == 0 :
                    #对于每一个点 (i, j)，到达这个点的方式只有从上一个点 (i - 1, j) 和左边的点 (i, j - 1)，所以 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]。
                    dp[i][j] = dp[i-1][j] + dp[i][j-1]
                #障碍物处dp[i][j] = 0
                else:
                    dp[i][j] = 0
        return dp[m-1][n-1]
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∗</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∗</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>



### [<font style="background-color:rgb(240, 240, 240);">最小路径和（64）</font>](https://leetcode.cn/problems/minimum-path-sum/)
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个包含非负整数的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> x </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 网格 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">grid</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">说明：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每次只能向下或者向右移动一步。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736217122017-0410692d-bfc9-4abe-beee-f81c5a62b17f.jpeg)

```plain
输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。
```

```python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        #dp[i][j]表示到为止i,j的最小路径和
        dp = copy.deepcopy(grid)
        m = len(grid)
        n = len(grid[0])
        
        #初始化第一行
        pre = 0
        for i in range(n):
            dp[0][i] = pre + dp[0][i]
            pre = dp[0][i]
        
        #初始化第一列
        pre = 0
        for i in range(m):
            dp[i][0] = pre + dp[i][0]
            pre = dp[i][0]
        
        for i in range(1,m):
            for j in range(1,n):
                #dp[i][j] = min(dp[i][j-i], dp[i-1][j]) + matrix[i][j]
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
        return dp[m-1][n-1]
```

  
时间复杂度：O(mn)，其中 m 和 n 分别是网格的行数和列数。需要对整个网格遍历一次，计算 dp 的每个元素的值。

空间复杂度：O(mn)，其中 m 和 n 分别是网格的行数和列数。创建一个二维数组 dp，和网格大小相同。

空间复杂度可以优化，例如每次只存储上一行的 dp 值，则可以将空间复杂度优化到 O(n)。



### [<font style="background-color:rgb(240, 240, 240);">单词搜索（79）</font>](https://leetcode.cn/problems/word-search/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m x n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">二维字符网格 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">board</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个字符串单词 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">存在于网格中，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">；否则，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736234479897-39a58cef-df67-4d9d-a0c5-3599993dd511.jpeg)

```plain
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true
```

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def dfs(depth, i, j):
            #非目标字符 退出当前搜索
            if board[i][j] != word[depth]:
                return False
            
            #找完所有目标字符，退出当前搜索
            if depth == length-1:
                # res = True
                return True
            
            #标记为已使用
            mark_grid[i][j] = 1
            
            a, b, c, d = False, False, False, False
            #向上搜索
            if j > 0 and mark_grid[i][j-1] != 1:
                a = dfs(depth+1, i, j-1)
            #向下搜索
            if j < n-1 and mark_grid[i][j+1] != 1:
                b = dfs(depth+1, i, j+1)
            #向左搜索
            if i > 0 and mark_grid[i-1][j] != 1:
                c = dfs(depth+1, i-1, j)
            #向右搜索
            if i < m-1 and mark_grid[i+1][j] != 1:
                d = dfs(depth+1, i+1, j)
            
            #清空标记
            mark_grid[i][j] = 0

            return a or b or c or d
            
        # res = False
        length = len(word)
        m = len(board)
        n = len(board[0])
        #mark_grid用于记录坐标i,j的元素是否被使用过
        mark_grid = [[0]*n for i in range(m)]
        
        for i in range(m):
            for j in range(n):
                #剪枝
                if board[i][j] == word[0]:
                    if dfs(0, i, j):
                        return True
        return False
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736234527573-4b2ecbd8-8515-4ac9-b6ce-e85401569300.png)





### [<font style="background-color:rgb(240, 240, 240);">最大矩形（85）</font>](https://leetcode.cn/problems/maximal-rectangle/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个仅包含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 、大小为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">rows x cols</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的二维二进制矩阵，找出只包含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的最大矩形，并返回其面积。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736240527523-215c9579-106f-49ba-88f7-f0debb45b22c.png)

```plain
输入：matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
输出：6
解释：最大矩形如上图所示。
```

```python
class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix:return 0
        m,n=len(matrix),len(matrix[0])
        # 记录当前位置上方连续“1”的个数
        pre=[0]*(n+1)
        res=0
        for i in range(m):
            for j in range(n):
                # 前缀和
                pre[j]=pre[j]+1 if matrix[i][j]=="1" else 0

            # 单调栈
            stack=[-1]#初始化栈，存入下标-1，便于处理所有元素弹出栈后的情况
            for k,num in enumerate(pre):
                #当栈顶索引index对应的元素pre[index]大于当前索引为k的元素num时
                while stack and pre[stack[-1]]>num:
                    #将栈顶元素index弹出
                    index=stack.pop()
                    #因为栈中索引对应的值是单调递增的，所以此时栈顶元素stack[-1]到k-1之间的数均是不小于pre[index]的，此时以pre[index]为高的矩阵的长度为k-stack[-1]-1，面积S=pre[index]*(k-stack[-1]-1)
                    res=max(res,pre[index]*(k-stack[-1]-1))
                stack.append(k)

        return res

```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(mn)</font>`
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(n)</font>`

<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">岛屿数量（200）</font>](https://leetcode.cn/problems/number-of-islands/)
岛屿问题：[https://leetcode.cn/problems/number-of-islands/?source=vscode](https://leetcode.cn/problems/number-of-islands/?source=vscode)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个由 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'1'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（陆地）和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'0'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（水）组成的的二维网格，请你计算网格中岛屿的数量。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">此外，你可以假设该网格的四条边均被水包围。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
输出：1
```

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def dfs(grid, r, c):
            #判断边界
            if not in_area(grid, r, c):
                return 
            
            #判断是否岛屿，如果不是岛屿，则退出搜索
            if grid[r][c] != '1':
                return 

            #已经遍历过的地方，标记为已经遍历过（沉入大海）
            #0 ：海洋
            #1 ：陆地
            #2 ：陆地：已经遍历过
            grid[r][c] = 2
            
            #访问上下左右四个相邻点
            dfs(grid, r-1, c)
            dfs(grid, r+1, c)
            dfs(grid, r, c-1)
            dfs(grid, r, c+1)
            
        #边界判断
        def in_area(grid, r, c):
            return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])
        
        res = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                #从岛屿出发进行DFS，把岛内其余的点置为大海
                if grid[r][c] == '1':
                    #岛屿数量=搜索次数
                    res += 1
                    dfs(grid, r, c)
        
        return res
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MN</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">M</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">和</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">分别为行数和列数。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MN</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，在最坏情况下，整个网格均为陆地，深度优先搜索的深度达到 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MN</font>_<font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

**  
**

### [<font style="background-color:rgb(240, 240, 240);">最大正方形（221）</font>](https://leetcode.cn/problems/maximal-square/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在一个由 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'0'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'1'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 组成的二维矩阵内，找到只包含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'1'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的最大正方形，并返回其面积。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736480161075-96afa900-9626-4e7d-937a-2f5fd4a46ba9.jpeg)

```plain
输入：matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
输出：4
```

```python
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m = len(matrix)
        n = len(matrix[0])
        #dp(i,j) 表示以 (i,j) 为右下角，且只包含 1 的正方形的边长最大值。如果我们能计算出所有 dp(i,j) 的值，那么其中的最大值即为矩阵中只包含 1 的正方形的边长最大值，其平方即为最大正方形的面积。
        dp = [[0]*n for i in range(m)]
        res = -inf
        
        for i in range(m):
            for j in range(n):
                #如果该位置的值是 1，则 dp(i,j) 的值由其上方、左方和左上方的三个相邻位置的 dp 值决定。具体而言，当前位置的元素值等于三个相邻位置的元素中的最小值加 1，状态转移方程如下：
                if matrix[i][j] == "1":
                    #边界初始化
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    #非边界
                    else:
                        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                res = max(res, dp[i][j])
        
        return res ** 2
```

时间复杂度：O(mn)，其中 m 和 n 是矩阵的行数和列数。需要遍历原始矩阵中的每个元素计算 dp 的值。

空间复杂度：O(mn)，其中 m 和 n 是矩阵的行数和列数。创建了一个和原始矩阵大小相同的矩阵 dp。由于状态转移方程中的 dp(i,j) 由其上方、左方和左上方的三个相邻位置的 dp 值决定，因此可以使用两个一维数组进行状态转移，空间复杂度优化至 O(n)。





10. [**<font style="background-color:rgb(240, 240, 240);">搜索二维矩阵 II（240）</font>**](https://leetcode.cn/problems/search-a-2d-matrix-ii/)**<font style="background-color:rgb(240, 240, 240);">（二分）</font>**

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">编写一个高效的算法来搜索 </font>`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> x </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 矩阵</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">matrix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中的一个目标值</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。该矩阵具有以下特性：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每行的元素从左到右升序排列。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每列的元素从上到下升序排列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736497141505-793f48b9-200a-475b-ab85-0c7051d29d9c.jpeg)

```plain
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true
```

由于矩阵 matrix 中每一行的元素都是升序排列的，因此我们可以对每一行都使用一次二分查找，判断 target 是否在该行中，从而判断 target 是否出现。

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        #二分法
        def binary_search(nums, target):
            left, right = 0, len(nums) - 1

            while left <= right:
                mid = left + (right - left) // 2  # 避免大数相加导致的溢出

                # 检查中间值是否是目标值
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    left = mid + 1  # 在右侧继续搜索
                else:
                    right = mid - 1  # 在左侧继续搜索

            return -1  # 未找到目标值
        
        #遍历每行，每行内进行二分查找
        for row in matrix:
            idx = binary_search(row, target)
            if idx < len(row) and row[idx] == target:
                return True
        return False
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">lo</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">g</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。对一行使用二分查找的时间复杂度为</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">lo</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">g</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，最多需要进行</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">次二分查找。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);">我们可以从矩阵 matrix 的右上角 (0,n−1) 进行搜索。在每一步的搜索过程中，如果我们位于位置 (x,y)，那么我们希望在以 matrix 的左下角为左下角、以 (x,y) 为右上角的矩阵中进行搜索，即行的范围为 [x,m−1]，列的范围为 [0,y]：</font>

<font style="background-color:rgb(240, 240, 240);">如果 matrix[x,y]=target，说明搜索完成；</font>

<font style="background-color:rgb(240, 240, 240);">如果 matrix[x,y]>target，由于每一列的元素都是升序排列的，那么在当前的搜索矩阵中，所有位于第 y 列的元素都是严格大于 target 的，因此我们可以将它们全部忽略，即将 y 减少 1；</font>

<font style="background-color:rgb(240, 240, 240);">如果 matrix[x,y]<target，由于每一行的元素都是升序排列的，那么在当前的搜索矩阵中，所有位于第 x 行的元素都是严格小于 target 的，因此我们可以将它们全部忽略，即将 x 增加 1。</font>

<font style="background-color:rgb(240, 240, 240);">在搜索的过程中，如果我们超出了矩阵的边界，那么说明矩阵中不存在 target。</font>

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        x, y = 0, n - 1
        while x < m and y >= 0:
            if matrix[x][y] == target:
                return True
            if matrix[x][y] > target:
                y -= 1
            else:
                x += 1
        return False

```

时间复杂度：O(m+n)。在搜索的过程中，如果我们没有找到 target，那么我们要么将 y 减少 1，要么将 x 增加 1。由于 (x,y) 的初始值分别为 (0,n−1)，因此 y 最多能被减少 n 次，x 最多能被增加 m 次，总搜索次数为 m+n。在这之后，x 和 y 就会超出矩阵的边界。

空间复杂度：O(1)。





### [<font style="background-color:rgb(240, 240, 240);">搜索二维矩阵 II（240）</font>](https://leetcode.cn/problems/search-a-2d-matrix-ii/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">编写一个高效的算法来搜索 </font>`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"> x </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 矩阵</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">matrix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中的一个目标值</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。该矩阵具有以下特性：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每行的元素从左到右升序排列。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每列的元素从上到下升序排列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1741069460683-1493224f-302e-49ff-8115-680e3c78f069.jpeg)

```plain
输入：matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
输出：true
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1741069791698-cf301b28-c692-4132-af41-216acf45a11c.png)

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # 如下图所示，我们将矩阵逆时针旋转 45° ，并将其转化为图形式，发现其类似于 二叉搜索树 ，即对于每个元素，其左分支元素更小、右分支元素更大。因此，通过从 “根节点” 开始搜索，遇到比 target 大的元素就向左，反之向右，即可找到目标值 target 。
        i, j = len(matrix) - 1, 0
        #从矩阵 matrix 左下角元素（索引设为 (i, j) ）开始遍历，并与目标值对比：
        while i >= 0 and j < len(matrix[0]):
            #当 matrix[i][j] > target 时，执行 i-- ，即消去第 i 行元素。
            if matrix[i][j] > target: i -= 1
            #当 matrix[i][j] < target 时，执行 j++ ，即消去第 j 列元素。
            elif matrix[i][j] < target: j += 1
            #当 matrix[i][j] = target 时，返回 true ，代表找到目标值。
            else: return True
        # 若行索引或列索引越界，则代表矩阵中无目标值，返回 false 。
        return False

```

时间复杂度 O(M+N) ：其中，N 和 M 分别为矩阵行数和列数，此算法最多循环 M+N 次。

空间复杂度 O(1) : i, j 指针使用常数大小额外空间。



## 1.5 子数组/子集/子序列
### [最大子数组和](https://leetcode.cn/problems/maximum-subarray/)
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。</font>

**<font style="background-color:rgb(240, 240, 240);">子数组</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是数组中的一个连续部分。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [1]
输出：1
```

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        res = -inf
        pre = 0
        for i in range(n):
            # f(i)=max{f(i−1)+nums[i],nums[i]}
            # f(i)表示以nums[i]结尾的最大连续子串和
            #考虑到 f(i) 只和 f(i−1) 相关，于是我们可以只用一个变量 pre 来维护对于当前 f(i) 的 f(i−1) 的值是多少，从而让空间复杂度降低到 O(1)，这有点类似「滚动数组」的思想。
            pre = max(pre + nums[i], nums[i])
            res = max(pre, res)
        return res
```

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        max_sum = dp[0]

        for i in range(1, n):
            dp[i] = max(nums[i], dp[i-1] + nums[i])
            max_sum = max(max_sum, dp[i])

        return max_sum
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数组的长度。我们只需要遍历一遍数组即可求得答案。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。我们只需要常数空间存放若干变量。</font>

****

### [组合总和](https://leetcode.cn/problems/combination-sum/)
回溯 DFS

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">无重复元素</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个目标整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，找出 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中可以使数字和为目标数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的 所有</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不同组合</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，并以列表形式返回。你可以按</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回这些组合。</font>

`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">candidates</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">同一个</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数字可以</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">无限制重复被选取</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果至少一个数字的被选数量不同，则两种组合是不同的。 </font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于给定的输入，保证和为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的不同组合数少于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">150</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：candidates = [2,3,6,7], target = 7
输出：[[2,2,3],[7]]
解释：
2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
7 也是一个候选， 7 = 7 。
仅有这两种组合。
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于这类寻找所有可行解的题，我们都可以尝试用「搜索回溯」的方法来解决。</font>

```python
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        
        def dfs(target, idx):
            #走到最后一个数字
            if idx == len(candidates):
                return
            #找到目标结果
            if target == 0:
                ans.append(combine.copy()) #copy() 
                return
            #分叉1 直接跳过
            dfs(target, idx+1)
            #分叉2 选择当前数字
            if (target - candidates[idx] >= 0):
                combine.append(candidates[idx])
                dfs(target-candidates[idx],idx)
                combine.pop()

        ans = []
        combine = []
        dfs(target, 0)
        return ans
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1735819150572-b8734bf2-9b15-4b77-afcc-6ecc2ee0aae6.png)



### [子集(78)](https://leetcode.cn/problems/subsets/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，数组中的元素</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">互不相同</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。返回该数组所有可能的</font><font style="background-color:rgb(240, 240, 240);">子集</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（幂集）。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">解集 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不能</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 包含重复的子集。你可以按 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 返回解集。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [0]
输出：[[],[0]]
```

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def dfs(doc_nums):
            if len(doc_nums) == 0:
                res.append(combine.copy())
                return
            
            #路径1：从剩余数字中选择一个
            for i in range(len(doc_nums)):
                combine.append(doc_nums[i])
                doc_nums_next = doc_nums[i+1:]
                dfs(doc_nums_next)
                combine.pop()
            
            #路径2：不添加数字
            res.append(combine.copy())
            return
        
        #升序排序
        nums.sort()
        res = []
        combine = []
        dfs(nums)
        return res
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736230419085-55ed3667-070a-4c17-9b89-99aa93b2b797.png)



### [<font style="background-color:rgb(240, 240, 240);">最长连续序列（128）</font>](https://leetcode.cn/problems/longest-consecutive-sequence/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个未排序的整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你设计并实现时间复杂度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(n)</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的算法解决此问题。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
```

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        #去重，获取哈希表
        num_set = set(nums)
        res = 0
        #遍历数组
        for num in num_set:
            #优化：先找到序列的最小的数，再往递增方向找
            if num-1 not in num_set: 
                curr_length = 1
                curr_num = num            
                #如果当前数字的前驱数字在哈希表中，开始计算连续序列的长度
                while curr_num + 1 in num_set:
                    curr_length += 1
                    curr_num = curr_num+1
                #更新连续序列的最大长度
                res = max(res, curr_length)
        
        return res
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">为数组的长度。具体分析已在上面正文中给出。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。哈希表存储数组中所有的数需要 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);"> 的空间。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">乘积最大子数组（152）</font>](https://leetcode.cn/problems/maximum-product-subarray/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你找出数组中乘积最大的非空连续</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">子数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">测试用例的答案是一个 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">32-位</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 整数。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: nums = [2,3,-2,4]
输出: 6
解释: 子数组 [2,3] 有最大乘积 6。
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736408345592-5eec3601-5bdb-46d9-9ae7-10655b6cb2e3.png)

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        res = nums[0]
        pre_max, pre_min = nums[0], nums[0]
        for i in range(1, n):
            #暂存最值，用于赋值
            mx, mn = pre_max, pre_min
            # f_max(i)表示以nums[i]结尾的最大连续子数组乘积
            # f_min(i)表示以nums[i]结尾的最小连续子数组乘积
            pre_max = max(mx * nums[i], max(nums[i], mn * nums[i]))
            pre_min = min(mn * nums[i], min(nums[i], mx * nums[i]))
            #防止溢出 2147483648是int类型最大值
            if pre_min < -2147483648:
                pre_min = nums[i]
            res = max(pre_max, res)
        return res
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">易得这里的渐进时间复杂度和渐进空间复杂度都是 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**  
**

### [<font style="background-color:rgb(240, 240, 240);">滑动窗口最大值（239）</font>](https://leetcode.cn/problems/sliding-window-maximum/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，有一个大小为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个数字。滑动窗口每次只向右移动一位。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">滑动窗口中的最大值 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
```

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        #对于「最大值」，我们可以想到一种非常合适的数据结构，那就是优先队列（堆），其中的大根堆可以帮助我们实时维护一系列元素中的最大值。
        # 注意 Python 默认的优先队列是小根堆
        
        #初始时，我们将数组 nums 的前 k 个元素放入优先队列中
        #为了方便判断堆顶元素与滑动窗口的位置关系，我们可以在优先队列中存储二元组 (num,index)，表示元素 num 在数组中的下标为 index。
        q = [(-nums[i], i) for i in range(k)]
        heapq.heapify(q)#将一个列表转换为堆：

        ans = [-q[0][0]]
        for i in range(k, n):
            #每当我们向右移动窗口时，我们就可以把一个新的元素放入优先队列中，此时堆顶的元素就是堆中所有元素的最大值。
            heapq.heappush(q, (-nums[i], i))#将元素添加到堆中：
            
            #然而这个最大值可能并不在滑动窗口中，在这种情况下，这个值在数组 nums 中的位置出现在滑动窗口左边界的左侧。
            #因此，当我们后续继续向右移动窗口时，这个值就永远不可能出现在滑动窗口中了，我们可以将其永久地从优先队列中移除。
            #我们不断地移除堆顶的元素，直到其确实出现在滑动窗口中
            #此时，堆顶元素就是滑动窗口中的最大值
            while q[0][1] <= i - k:  #堆顶元素的下标 <= i-k   说明堆顶元素在滑动窗内
                heapq.heappop(q)#从堆中弹出最小元素：
            ans.append(-q[0][0])#记录最大值：
        
        return ans
```

时间复杂度：O(nlogn)，其中 n 是数组 nums 的长度。在最坏情况下，数组 nums 中的元素单调递增，那么最终优先队列中包含了所有元素，没有元素被移除。由于将一个元素放入优先队列的时间复杂度为 O(logn)，因此总时间复杂度为 O(nlogn)。

空间复杂度：O(n)，即为优先队列需要使用的空间。这里所有的空间复杂度分析都不考虑返回的答案需要的 O(n) 空间，只计算额外的空间使用。



### [<font style="background-color:rgb(240, 240, 240);">最长递增子序列（300）</font>](https://leetcode.cn/problems/longest-increasing-subsequence/)<font style="background-color:rgb(240, 240, 240);">（DP）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找到其中最长严格递增子序列的长度。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">子序列 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[3,6,2,7]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[0,3,1,6,2,2,7]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的</font><font style="background-color:rgb(240, 240, 240);">子序列</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
```

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        n = len(nums)
        #dp[i]表示以下标为i的元素结尾的最长递增子序列长度
        dp = [1] * n
        # 递归公式
        # dp[i] = max(dp[i], dp[j]+1),其中0≤j<i且num[j]<num[i]
        for i in range(0, n):
            for j in range(0, i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j]+1)
        
        return max(dp)
```

时间复杂度：O(n ^2 )，其中 n 为数组 nums 的长度。动态规划的状态数为 n，计算状态 dp[i] 时，需要 O(n) 的时间遍历 dp[0…i−1] 的所有状态，所以总时间复杂度为 O(n ^2)。

空间复杂度：O(n)，需要额外使用长度为 n 的 dp 数组。





### [<font style="background-color:rgb(240, 240, 240);">分割等和子集（416）</font>](https://leetcode.cn/problems/partition-equal-subset-sum/)<font style="background-color:rgb(240, 240, 240);">（DP）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">只包含正整数 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非空 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736823790707-0f64fcae-4f39-4bd3-9103-7e32ae9b3ce5.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736823804980-e819fe2d-85f2-4563-97d4-9b0f7be89724.png)

```python
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 2:
            return False
        
        total = sum(nums)
        if total % 2 != 0:
            return False
        
        target = total // 2
        dp = [True] + [False] * target
        for i, num in enumerate(nums):
            for j in range(target, num - 1, -1):
                dp[j] |= dp[j - num]
        
        return dp[target]
```

时间复杂度：O(n×target)，其中 n 是数组的长度，target 是整个数组的元素和的一半。需要计算出所有的状态，每个状态在进行转移时的时间复杂度为 O(1)。

空间复杂度：O(target)，其中 target 是整个数组的元素和的一半。空间复杂度取决于 dp 数组，在不进行空间优化的情况下，空间复杂度是 O(n×target)，在进行空间优化的情况下，空间复杂度可以降到 O(target)。







### [<font style="background-color:rgb(240, 240, 240);">和为 K 的子数组（560）</font>](https://leetcode.cn/problems/subarray-sum-equals-k/)（前缀和+哈希表）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和一个整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你统计并返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">该数组中和为 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>_`_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的子数组的个数 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">子数组是数组中元素的连续非空序列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,1,1], k = 2
输出：2
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736847716232-f2c9f112-e463-4467-9187-dda8f4246978.png)

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        pre = 0
        n = len(nums)
        #建立哈希表，以和为键，出现次数为对应的值，记录 pre[i] 出现的次数
        hashmap = dict()
        hashmap[0] = 1
        for i in range(n):
            #前缀和
            pre += nums[i]
            #统计有多少个前缀和为 pre[i]−k 的 pre[j] (以 i 结尾的和为 k 的连续子数组个数)
            if pre-k in hashmap:
                count += hashmap[pre-k]

            #pre加入hash表
            if pre in hashmap:
                hashmap[pre] += 1
            else:
                hashmap[pre] = 1
        return count
```

时间复杂度：O(n)，其中 n 为数组的长度。我们遍历数组的时间复杂度为 O(n)，中间利用哈希表查询删除的复杂度均为 O(1)，因此总时间复杂度为 O(n)。

空间复杂度：O(n)，其中 n 为数组的长度。哈希表在最坏情况下可能有 n 个不同的键值，因此需要 O(n) 的空间复杂度。

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        res = 0
        #统计以i结尾的和为k的子数组数量
        for i in range(n):
            #子数组下标：[j:i]
            sum = 0
            for j in range(i, -1, -1):
                sum += nums[j]
                if sum == k:
                    res += 1
        return res
```

时间复杂度：O(n^2 )，其中 n 为数组的长度。枚举子数组开头和结尾需要 O(n ^2 ) 的时间，其中求和需要 O(1) 的时间复杂度，因此总时间复杂度为 O(n ^2 )。

空间复杂度：O(1)。只需要常数空间存放若干变量。





### [<font style="background-color:rgb(240, 240, 240);">最短无序连续子数组（581）</font>](https://leetcode.cn/problems/shortest-unsorted-continuous-subarray/)(快排)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数数组</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，你需要找出一个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">连续子数组</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，如果对这个子数组进行升序排序，那么整个数组都会变为升序排序。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你找出符合题意的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最短</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 子数组，并输出它的长度。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [2,6,4,8,10,9,15]
输出：5
解释：你只需要对 [6, 4, 8, 10, 9] 进行升序排序，那么整个表都会变为升序排序。
```

```python
class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
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

        n = len(nums)
        ori_nums = copy.deepcopy(nums)
        quicksort(nums, 0, len(nums) - 1)
        #找左边界
        i = 0
        while i <= n-1 and nums[i] == ori_nums[i]:
            i += 1

        #找右边界
        j = n-1
        while j >= 0 and nums[j] == ori_nums[j]:
            j -= 1
        return max(j-i+1, 0)
```

时间复杂度：O(nlogn)，其中 n 为给定数组的长度。我们需要 O(nlogn) 的时间进行排序，以及 O(n) 的时间遍历数组，因此总时间复杂度为 O(nlogn)。

空间复杂度：O(n)，其中 n 为给定数组的长度。我们需要额外的一个数组保存排序后的数组 numsSorted。



# 二、字符串
## 2.1 字符串
### KMP
```python
def kmp_substring_match(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    if len_str2 == 0:
        return True  # 空字符串被认为是任何字符串的子串
    if len_str2 > len_str1:
        return False  # 子串长度大于母串，不可能存在
    
    # 步骤 1：构建前缀函数数组
    prefix = [0] * len_str2
    j = 0
    for i in range(1, len_str2):
        while j > 0 and str2[i] != str2[j]:
            j = prefix[j-1]
        if str2[i] == str2[j]:
            j += 1
        prefix[i] = j
    
    # 步骤 2：执行KMP算法进行匹配
    j = 0
    for i in range(len_str1):
        while j > 0 and str1[i] != str2[j]:
            j = prefix[j-1]
        if str1[i] == str2[j]:
            j += 1
            if j == len_str2:
                return True  # 找到子串
    return False  # 匹配失败

# 示例用法
str1 = "香辣鸡块+可乐"
str2 = "香辣鸡块+可乐"
print(kmp_substring_match(str1, str2))  # 输出：True
```

### Z型变换
**<font style="color:#601BDE;">解法：顺序遍历</font>**

:::color3
<font style="color:rgb(38, 38, 38);">将一个给定字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);">s</font>`<font style="color:rgb(38, 38, 38);"> 根据给定的行数 </font>`<font style="color:rgba(38, 38, 38, 0.75);">numRows</font>`<font style="color:rgb(38, 38, 38);"> ，以从上往下、从左到右进行 Z 字形排列。</font>

<font style="color:rgb(38, 38, 38);">比如输入字符串为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">"PAYPALISHIRING"</font>`<font style="color:rgb(38, 38, 38);"> 行数为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">3</font>`<font style="color:rgb(38, 38, 38);"> 时，排列如下：</font>

:::

```plain
P   A   H   N
A P L S I I G
Y   I   R
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734691158675-372be8ed-7678-4727-8ad7-d14a2e13a7dd.png)

```python
class Solution:
    def convert(self, s: str, numRows: int) -> str:

        if len(s) <= 2: return s
        if numRows <= 1 :return s
        res = ["" for i in range(numRows)]

        i = 0
        flag = -1
        for c in s:
            res[i] += c
            if i == 0 or i == numRows-1 :
                flag = -flag
            i += flag

        return "".join(res)
```

+ **<font style="background-color:rgb(240, 240, 240);">时间复杂度</font>****<font style="background-color:rgb(240, 240, 240);"> </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：遍历一遍字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">；</font>
+ **<font style="background-color:rgb(240, 240, 240);">空间复杂度 </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ：各行字符串共占用 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 额外空间。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### 字符串转整数
![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734941555061-a348d81a-440f-4939-9a37-3820e0968407.png)

```python
INT_MAX = 2 ** 31 - 1
INT_MIN = -2 ** 31

class Automaton:
    def __init__(self):
        self.state = 'start'
        self.sign = 1
        self.ans = 0
        self.table = {
            'start': ['start', 'signed', 'in_number', 'end'],
            'signed': ['end', 'end', 'in_number', 'end'],
            'in_number': ['end', 'end', 'in_number', 'end'],
            'end': ['end', 'end', 'end', 'end'],
        }
        
    def get_col(self, c):
        if c.isspace():
            return 0
        if c == '+' or c == '-':
            return 1
        if c.isdigit():
            return 2
        return 3

    def get(self, c):
        self.state = self.table[self.state][self.get_col(c)]
        if self.state == 'in_number':
            self.ans = self.ans * 10 + int(c)
            self.ans = min(self.ans, INT_MAX) if self.sign == 1 else min(self.ans, -INT_MIN)
        elif self.state == 'signed':
            self.sign = 1 if c == '+' else -1

class Solution:
    def myAtoi(self, str: str) -> int:
        automaton = Automaton()
        for c in str:
            automaton.get(c)
        return automaton.sign * automaton.ans

```

时间复杂度：O(n)，其中 n 为字符串的长度。我们只需要依次处理所有的字符，处理每个字符需要的时间O(1)。

空间复杂度：O(1)。自动机的状态只需要常数空间存储。

### 正则表达式匹配
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和一个字符规律 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">p</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你来实现一个支持</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'.'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'*'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的正则表达式匹配。</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'.'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">匹配任意单个字符</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'*'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">匹配零个或多个前面的那一个元素</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">所谓匹配，是要涵盖 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整个 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的，而不是部分字符串。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "aa", p = "a"
输出：false
解释："a" 无法匹配 "aa" 整个字符串。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2:</font>**

```plain
输入：s = "aa", p = "a*"
输出：true
解释：因为 '*' 代表可以匹配零个或多个前面的那一个元素, 在这里前面的元素就是 'a'。因此，字符串 "aa" 可被视为 'a' 重复了一次。
```

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s) + 1, len(p) + 1
        dp = [[False] * n for _ in range(m)]
        dp[0][0] = True
        # 初始化首行
        for j in range(2, n, 2):
            dp[0][j] = dp[0][j - 2] and p[j - 1] == '*'
        # 状态转移
        for i in range(1, m):
            for j in range(1, n):
                if p[j - 1] == '*':
                    if dp[i][j - 2]: dp[i][j] = True                              # 1.
                    elif dp[i - 1][j] and s[i - 1] == p[j - 2]: dp[i][j] = True   # 2.
                    elif dp[i - 1][j] and p[j - 2] == '.': dp[i][j] = True        # 3.
                else:
                    if dp[i - 1][j - 1] and s[i - 1] == p[j - 1]: dp[i][j] = True # 1.
                    elif dp[i - 1][j - 1] and p[j - 1] == '.': dp[i][j] = True    # 2.
        return dp[-1][-1]

```

时间复杂度 O(MN) ： 其中 M,N 分别为 s 和 p 的长度，状态转移需遍历整个 dp 矩阵。

空间复杂度 O(MN) ： 状态矩阵 dp 使用 O(MN) 的额外空间。

### 罗马数字转整数
[https://leetcode.cn/problems/roman-to-integer/description/](https://leetcode.cn/problems/roman-to-integer/description/)

贪心  哈希表

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">罗马数字包含以下七种字符: </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">I</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">， </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">V</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">， </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">， </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">D</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">M</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

```plain
字符          数值
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如， 罗马数字</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">写做 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">II</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，即为两个并列的 1 。</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">12</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">写做 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">XII</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，即为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> + </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">II</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">27</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">写做  </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">XXVII</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">, 即为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">XX</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> + </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">V</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> + </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">II</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，例如 4 不写做 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IIII</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，而是 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IV</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。数字 1 在数字 5 的左边，所表示的数等于大数 5 减小数 1 得到的数值 4 。同样地，数字 9 表示为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IX</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。这个特殊的规则只适用于以下六种情况：</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">I</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 可以放在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">V</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (5) 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (10) 的左边，来表示 4 和 9。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 可以放在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (50) 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (100) 的左边，来表示 40 和 90。 </font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 可以放在 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">D</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (500) 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">M</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> (1000) 的左边，来表示 400 和 900。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个罗马数字，将其转换成整数。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: s = "III"
输出: 3
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2:</font>**

```plain
输入: s = "IV"
输出: 4
```

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        hashmap = {'M':1000, 'CM':900, 'D':500, 'CD':400, 'C':100, 'XC':90, 'L':50, 'XL':40, 'X':10, 'IX':9, 'V':5, 'IV':4, 'I':1}

        res = 0
        i = 0
        while i < len(s):
            if s[i:i+2] in hashmap.keys():
                res += hashmap[s[i:i+2]]
                i += 2
                continue
            if s[i] in hashmap.keys():
                res += hashmap[s[i]]
                i+=1
        return res

```

+ <font style="background-color:rgb(240, 240, 240);">通过 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key</font>`<font style="background-color:rgb(240, 240, 240);"> 查找 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">value</font>`<font style="background-color:rgb(240, 240, 240);"> 的时间复杂度为 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font>

<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);"></font>

### 最长公共前缀
[https://leetcode.cn/problems/longest-common-prefix/description/](https://leetcode.cn/problems/longest-common-prefix/description/)

:::color3
编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

示例 1：

输入：strs = ["flower","flow","flight"]

输出："fl"

示例 2：

输入：strs = ["dog","racecar","car"]

输出：""

解释：输入不存在公共前缀。

:::

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:

        min_len = min(len(s) for s in strs)
        strs = [s[:min_len] for s in strs]
        n = len(strs)
        if n == 0:
            return ""
        if n == 1:
            return strs[0]
        if len(strs[0]) == 0:
            return ""
        idx = 0

        while idx < len(strs[0]) and self.is_char_same(strs, idx):
            idx += 1

        return strs[0][:idx] 


    
    def is_char_same(self, strs, idx):
        flag = True
        for i in range(len(strs)-1):
            if strs[i][idx] != strs[i+1][idx]:
                flag = False
                break
        return flag
```

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        
        length, count = len(strs[0]), len(strs)
        for i in range(length):
            c = strs[0][i]
            if any(i == len(strs[j]) or strs[j][i] != c for j in range(1, count)):
                return strs[0][:i]
        
        return strs[0]

```

时间复杂度：O(mn)，其中 m 是字符串数组中的字符串的平均长度，n 是字符串的数量。最坏情况下，字符串数组中的每个字符串的每个字符都会被比较一次。

空间复杂度：O(1)。使用的额外空间复杂度为常数。





### 电话号码的字母组合
[https://leetcode.cn/problems/letter-combinations-of-a-phone-number/description/](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/description/)

回溯

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个仅包含数字 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2-9</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的字符串，返回所有它能表示的字母组合。答案可以按</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735212667230-5beb625c-ff8a-443b-9923-23ea021b6f27.png)

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735212649698-e7e7f0fd-ad6d-470e-a68f-1e171a4e6cf0.png)

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if len(digits) == 0 : return []

        #hash表
        phoneMap = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        res = []
        curr_string = []
        #回溯
        def backtrack(index : int):
            #到了最后一个数字
            if index == len(digits):
                res.append("".join(curr_string))
            else:
                digit = digits[index]
                for letter in phoneMap[digit]:
                    #进入下一个层
                    curr_string.append(letter)
                    backtrack(index + 1)
                    #回退上一层
                    curr_string.pop()
        
        backtrack(0)
        
        return res



```

时间复杂度：O(3^m×4^n )，其中 m 是输入中对应 3 个字母的数字个数（包括数字 2、3、4、5、6、8），n 是输入中对应 4 个字母的数字个数（包括数字 7、9），m+n 是输入数字的总个数。当输入包含 m 个对应 3 个字母的数字和 n 个对应 4 个字母的数字时，不同的字母组合一共有 3 m ×4 n种，需要遍历每一种字母组合。



空间复杂度：O(m+n)，其中 m 是输入中对应 3 个字母的数字个数，n 是输入中对应 4 个字母的数字个数，m+n 是输入数字的总个数。除了返回值以外，空间复杂度主要取决于哈希表以及回溯过程中的递归调用层数，哈希表的大小与输入无关，可以看成常数，递归调用层数最大为 m+n。



### [KMP/找出字符串中第一个匹配项的下标](https://leetcode.cn/problems/find-the-index-of-the-first-occurrence-in-a-string/)
**<font style="color:#601BDE;">解法：双指针/KMP</font>**

:::color3
<font style="color:rgb(38, 38, 38);">给你两个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);">haystack</font>`<font style="color:rgb(38, 38, 38);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);">needle</font>`<font style="color:rgb(38, 38, 38);"> ，请你在 </font>`<font style="color:rgba(38, 38, 38, 0.75);">haystack</font>`<font style="color:rgb(38, 38, 38);"> 字符串中找出 </font>`<font style="color:rgba(38, 38, 38, 0.75);">needle</font>`<font style="color:rgb(38, 38, 38);"> 字符串的第一个匹配项的下标（下标从 0 开始）。如果 </font>`<font style="color:rgba(38, 38, 38, 0.75);">needle</font>`<font style="color:rgb(38, 38, 38);"> 不是 </font>`<font style="color:rgba(38, 38, 38, 0.75);">haystack</font>`<font style="color:rgb(38, 38, 38);"> 的一部分，则返回  </font>`<font style="color:rgba(38, 38, 38, 0.75);">-1</font>`**<font style="color:rgb(38, 38, 38);"> </font>**<font style="color:rgb(38, 38, 38);">。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：haystack = "sadbutsad", needle = "sad"
输出：0
解释："sad" 在下标 0 和 6 处匹配。
第一个匹配项的下标是 0 ，所以返回 0 。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：haystack = "leetcode", needle = "leeto"
输出：-1
解释："leeto" 没有在 "leetcode" 中出现，所以返回 -1 。
```

```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n1 = len(haystack)
        n2 = len(needle)

        for i in range(n1):
            left = i
            right = 0
            while left < n1 and right < n2 and haystack[left] == needle[right]:
                left += 1
                right += 1
            if right == n2:
                return i

        return -1
```

### ![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735633947838-8aec569e-c327-4654-8eed-dc0e8e668917.png)
```python
class Solution:
    def get_pre(self, s):
        j, pre = 0, [0] * len(s)
        for i in range(1, len(s)):
            while j > 0 and s[i] != s[j]:
                j = pre[j - 1]
            if s[i] == s[j]:
                j += 1
            pre[i] = j
        return pre
    def strStr(self, haystack: str, needle: str) -> int:
        j, pre = 0, self.get_pre(needle)
        for i in range(len(haystack)):
            while j > 0 and haystack[i] != needle[j]:
                j = pre[j - 1]
            if haystack[i] == needle[j]:
                j += 1
            if j == len(needle):
                return i - j + 1
        return -1
```

时间复杂度：O(n+m)，其中 n 是字符串 haystack 的长度，m 是字符串 needle 的长度。我们至多需要遍历两字符串一次。

空间复杂度：O(m)，其中 m 是字符串 needle 的长度。我们只需要保存字符串 needle 的前缀函数。



### [字母异位词分组](https://leetcode.cn/problems/group-anagrams/)
哈希表

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个字符串数组，请你将</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">字母异位词</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">组合在一起。可以按任意顺序返回结果列表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">字母异位词</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是由重新排列源单词的所有字母得到的一个新单词。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2:</font>**

```plain
输入: strs = [""]
输出: [[""]]
```

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = dict()
        res = []
        for str in strs:
            #排序
            sort_str = "".join(sorted(str))
            #用排序后的str作为key
            if sort_str in hashmap.keys():
                hashmap[sort_str].append(str)
            else:
                hashmap[sort_str] = [str]
        return list(hashmap.values())
```

时间复杂度：O(nklogk)，其中 n 是 strs 中的字符串的数量，k 是 strs 中的字符串的的最大长度。需要遍历 n 个字符串，对于每个字符串，需要 O(klogk) 的时间进行排序以及 O(1) 的时间更新哈希表，因此总时间复杂度是 O(nklogk)。

空间复杂度：O(nk)，其中 n 是 strs 中的字符串的数量，k 是 strs 中的字符串的的最大长度。需要用哈希表存储全部字符串。

方法2：计数

由于互为字母异位词的两个字符串包含的字母相同，因此两个字符串中的相同字母出现的次数一定是相同的，故可以将每个字母出现的次数使用字符串表示，作为哈希表的键。

由于字符串只包含小写字母，因此对于每个字符串，可以使用长度为 26 的数组记录每个字母出现的次数。需要注意的是，在使用数组作为哈希表的键时，不同语言的支持程度不同，因此不同语言的实现方式也不同。

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mp = collections.defaultdict(list)

        for st in strs:
            counts = [0] * 26
            for ch in st:
                counts[ord(ch) - ord("a")] += 1
            # 需要将 list 转换成 tuple 才能进行哈希
            mp[tuple(counts)].append(st)
        
        return list(mp.values())

```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736147463045-b77a0f4d-1b5f-4d82-87fa-ec2233860838.png)





### [<font style="background-color:rgb(240, 240, 240);">编辑距离（72）</font>](https://leetcode.cn/problems/edit-distance/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个单词 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请返回将 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word1</font>_`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 转换成 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word2</font>_`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">所使用的最少操作数</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以对一个单词进行如下三种操作：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">插入一个字符</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">删除一个字符</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">替换一个字符</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736220091962-c14e89df-7f9b-4e59-a31e-6c4c1655c8fa.png)

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        n1 = len(word1)
        n2 = len(word2)
        #dp[i][j] 代表 word1 中前 i 个字符，变换到 word2 中前 j 个字符，最短需要操作的次数
        #dp[i-1][j-1] 表示替换操作，dp[i-1][j] 表示删除操作，dp[i][j-1] 表示插入操作。
        dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
        #  第一行，是 word1 为空变成 word2 最少步数，就是插入操作
        for j in range(1, n2 + 1):
            dp[0][j] = dp[0][j-1] + 1
        # 第一列，是 word2 为空，需要的最少步数，就是删除操作
        for i in range(1, n1 + 1):
            dp[i][0] = dp[i-1][0] + 1
        #开始dp
        for i in range(1, n1 + 1):
            for j in range(1, n2 + 1):
                #当 word1[i] == word2[j]，dp[i][j] = dp[i-1][j-1]；
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                #当 word1[i] != word2[j]，dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + 1
                else:
                    dp[i][j] = min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1] ) + 1
        #print(dp)      
        return dp[-1][-1]
```

时间复杂度 ：O(mn)，其中 m 为 word1 的长度，n 为 word2 的长度。

空间复杂度 ：O(mn)，我们需要大小为 O(mn) 的 D 数组来记录状态值。



### [<font style="background-color:rgb(240, 240, 240);">单词拆分（139）</font>](https://leetcode.cn/problems/word-break/)
**<font style="color:#601BDE;">解法：动态规划</font>**

:::color3
<font style="color:rgb(38, 38, 38);">给你一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);">s</font>`<font style="color:rgb(38, 38, 38);"> 和一个字符串列表 </font>`<font style="color:rgba(38, 38, 38, 0.75);">wordDict</font>`<font style="color:rgb(38, 38, 38);"> 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 </font>`<font style="color:rgba(38, 38, 38, 0.75);">s</font>`<font style="color:rgb(38, 38, 38);"> 则返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">true</font>`<font style="color:rgb(38, 38, 38);">。</font>

**<font style="color:rgb(38, 38, 38);">注意：</font>**<font style="color:rgb(38, 38, 38);">不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)
        #dp[i] 表示字符串 s 前 i 个字符组成的字符串 s[0..i−1] 是否能被空格拆分成若干个字典中出现的单词。
        dp = [False for i in range(n+1)]
        dp[0] = True
        for i in range(1, n+1):
            #我们需要枚举 s[0..i−1] 中的分割点 j ，看 s[0..j−1] 组成的字符串 s 1 （默认 j=0 时 s 1  为空串）和 s[j..i−1] 组成的字符串 s 2是否都合法，
            for j in range(i):
                #状态转移方程： dp[i]=dp[j] && check(s[j..i−1])
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        return dp[n]
```

时间复杂度：O(n ^2 ) ，其中 n 为字符串 s 的长度。我们一共有 O(n) 个状态需要计算，每次计算需要枚举 O(n) 个分割点，哈希表判断一个字符串是否出现在给定的字符串列表需要 O(1) 的时间，因此总时间复杂度为 O(n^2 )。

空间复杂度：O(n) ，其中 n 为字符串 s 的长度。我们需要 O(n) 的空间存放 dp 值以及哈希表亦需要 O(n) 的空间复杂度，因此总空间复杂度为 O(n)。





### [<font style="background-color:rgb(240, 240, 240);">字符串解码（394）</font>](https://leetcode.cn/problems/decode-string/)<font style="background-color:rgb(240, 240, 240);">（栈/递归）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个经过编码的字符串，返回它解码后的字符串。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">编码规则为:</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k[encoded_string]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示其中方括号内部的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">encoded_string</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">正好重复</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">次。注意</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保证为正整数。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，例如不会出现像 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">3a</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 或 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2[4]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的输入。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

```python
class Solution:
    def decodeString(self, s: str) -> str:
        #构建辅助栈 stack， 遍历字符串 s 中每个字符 c
        stack, res, multi = [], "", 0
        for c in s:
            #当 c 为 [ 时，将当前 multi 和 res 入栈，并分别置空置 0：
            if c == '[':
                #记录此 [ 前的临时结果 res 至栈，用于发现对应 ] 后的拼接操作；
                #记录此 [ 前的倍数 multi 至栈，用于发现对应 ] 后，获取 multi × [...] 字符串。
                stack.append([multi, res])
                #进入到新 [ 后，res 和 multi 重新记录。
                res, multi = "", 0
            #当 c 为 ] 时，stack 出栈，拼接字符串 res = last_res + cur_multi * res，其中:
            elif c == ']':
                #last_res是上个 [ 到当前 [ 的字符串，例如 "3[a2[c]]" 中的 a；
                #cur_multi是当前 [ 到 ] 内字符串的重复倍数，例如 "3[a2[c]]" 中的 2。
                cur_multi, last_res = stack.pop()
                res = last_res + cur_multi * res
            #当 c 为数字时，将数字字符转化为数字 multi，用于后续倍数计算；
            elif '0' <= c <= '9':
                multi = multi * 10 + int(c)        
            #当 c 为字母时，在 res 尾部添加 c；    
            else:
                res += c
        return res
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，一次遍历</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">；</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，辅助栈在极端情况下需要线性空间，例如 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2[2[2[a]]]</font>`

```python
class Solution:
    def decodeString(self, s: str) -> str:
        def dfs(s, i):
            res, multi = "", 0
            while i < len(s):
                if '0' <= s[i] <= '9':
                    multi = multi * 10 + int(s[i])
                #当 s[i] == '[' 时，开启新一层递归，记录此 [...] 内字符串 tmp 和递归后的最新索引 i，并执行 res + multi * tmp 拼接字符串。
                elif s[i] == '[':
                    i, tmp = dfs(s, i + 1)
                    res += multi * tmp
                    multi = 0
                #当 s[i] == '[' 时，开启新一层递归，记录此 [...] 内字符串 tmp 和递归后的最新索引 i，并执行 res + multi * tmp 拼接字符串。
                elif s[i] == ']':
                    return i, res
                else:
                    res += s[i]
                i += 1
            return res
        return dfs(s,0)
```

    - 时间复杂度 _<font style="color:rgba(38, 38, 38, 0.75);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);">)</font>，递归会更新索引，因此实际上还是一次遍历 `<font style="color:rgba(38, 38, 38, 0.75);">s</font>`；
    - 空间复杂度 _<font style="color:rgba(38, 38, 38, 0.75);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);">N</font>_<font style="color:rgba(38, 38, 38, 0.75);">)</font>，极端情况下递归深度将会达到线性级别。





12. [**<font style="background-color:rgb(240, 240, 240);">找到字符串中所有字母异位词（438）</font>**](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定两个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">p</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中所有 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">p</font>`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的 </font>**<font style="background-color:rgb(240, 240, 240);">异位词</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的子串，返回这些子串的起始索引。不考虑答案输出的顺序。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。
```

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        #根据题目要求，我们需要在字符串 s 寻找字符串 p 的异位词。因为字符串 p 的异位词的长度一定与字符串 p 的长度相同，所以我们可以在字符串 s 中构造一个长度为与字符串 p 的长度相同的滑动窗口，并在滑动中维护窗口中每种字母的数量；当窗口中每种字母的数量与字符串 p 中每种字母的数量相同时，则说明当前窗口为字符串 p 的异位词。
        #在算法的实现中，我们可以使用数组来存储字符串 p 和滑动窗口中每种字母的数量。

        #当字符串 s 的长度小于字符串 p 的长度时，字符串 s 中一定不存在字符串 p 的异位词。但是因为字符串 s 中无法构造长度与字符串 p 的长度相同的窗口，所以这种情况需要单独处理。
        s_len, p_len = len(s), len(p)
        
        if s_len < p_len:
            return []

        ans = []
        s_count = [0] * 26
        p_count = [0] * 26
        for i in range(p_len):
            s_count[ord(s[i]) - 97] += 1
            p_count[ord(p[i]) - 97] += 1

        if s_count == p_count:
            ans.append(0)

        for i in range(s_len - p_len):
            s_count[ord(s[i]) - 97] -= 1
            s_count[ord(s[i + p_len]) - 97] += 1
            
            if s_count == p_count:
                ans.append(i + 1)

        return ans

```

## 2.2 回文串
### **<font style="background-color:rgb(240, 240, 240);">最长回文子串</font>**
**<font style="background-color:rgb(240, 240, 240);">动态规划</font>**

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中最长的 </font><font style="background-color:rgb(240, 240, 240);">回文</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">子串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：s = "cbbd"
输出："bb"
```

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        # 定义：dp[i][j]表示s[i]到s[j]是否为回文
        # 递推：dp[i][j]=dp[i+1][j-1]&(s[i]==s[j]) if j - i >= 2 else s[i]==s[j]
        dp = [[False]*n for i in range(n)]
        max_len = 0
        res = ""
        #i是左边界，从大到小   这样保证子串长度（j-i+1）是从小到大的，才能找到子串长度的最大值
        for i in range(n,-1,-1):
            #j是右边界，从小到大
            for j in range(i,n):
                #首尾是否相等
                if s[i] == s[j]:
                    #子串长度<=2
                    if j-i+1 <= 2:
                        dp[i][j] = True
                        if j-i+1 >max_len:
                            max_len = j-i+1
                            res = s[i:j+1]
                    #子串长度>2
                    elif dp[i+1][j-1]:
                        dp[i][j] = True
                        if j-i+1 >max_len:
                            max_len = j-i+1
                            res = s[i:j+1]

        return res
```

<font style="background-color:rgb(240, 240, 240);">时间复杂度：O(n 2)，其中 n 是字符串的长度。动态规划的状态总数为 O(n2)，对于每个状态，我们需要转移的时间为 O(1)。</font>

<font style="background-color:rgb(240, 240, 240);">空间复杂度：O(n 2)，即存储动态规划状态需要的空间。</font>



### [<font style="background-color:rgb(240, 240, 240);">最长回文串（409）</font>](https://leetcode.cn/problems/longest-palindrome/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个包含大写字母和小写字母的字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">通过这些字母构造成的</font>__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>__**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最长的</font>**__**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**__**<font style="background-color:rgb(240, 240, 240);">回文串</font>**_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的长度。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在构造过程中，请注意 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">区分大小写</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。比如 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">"Aa"</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 不能当做一个回文字符串。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入:s = "abccccdd"
输出:7
解释:
我们可以构造的最长的回文串是"dccaccd", 它的长度是 7。
```

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        #哈希表
        hashmap = dict()
        for char in s:
            if char not in hashmap:
                hashmap[char] = 1
            else:
                hashmap[char] += 1
        
        sum_part1 = 0
        sum_part2 = 0
        for value in hashmap.values():
            sum_part1 += value//2
            sum_part2 += value%2
        
        sum_part2 = 1 if sum_part2 > 0 else 0
        
        # return hashmap
        # return sum_part1, sum_part2
        return sum_part1*2 + sum_part2
```

时间复杂度：O(N)，其中 N 为字符串 s 的长度。我们需要遍历每个字符一次。

空间复杂度：O(S)，其中 S 为字符集大小。在 Java 代码中，我们使用了一个长度为 128 的数组，存储每个字符出现的次数，这是因为字符的 ASCII 值的范围为 [0, 128)。而由于题目中保证了给定的字符串 s 只包含大小写字母，因此我们也可以使用哈希映射（HashMap）来存储每个字符出现的次数，例如 Python 和 C++ 的代码。如果使用哈希映射，最多只会存储 52 个（即小写字母与大写字母的数量之和）键值对。





### [回文子串（647）](https://leetcode.cn/problems/palindromic-substrings/description/)（中心拓展）
给你一个字符串 `s` ，请你统计并返回这个字符串中 **回文子串** 的数目。

**回文字符串** 是正着读和倒过来读一样的字符串。

**子字符串** 是字符串中的由连续字符组成的一个序列。

**示例 1：**

```plain
输入：s = "abc"
输出：3
解释：三个回文子串: "a", "b", "c"
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736326128766-21551a4e-2388-4828-ac66-d5f8f5138be7.png)

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        res = 0
        #长度为n的字符串，回文中心组合有2*n-1种
        for i in range(2*n-1):
            left = i // 2
            right = i // 2 + i%2  #i为偶数时，left和right相同
            #从中心开始左右拓展
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
                res += 1
            
        return res
            
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n^</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

## <font style="background-color:rgb(240, 240, 240);">2.3 子串问题</font>
### 最长不重复子串
滑动窗+双指针

<font style="color:rgb(38, 38, 38);">给定一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);">s</font>`<font style="color:rgb(38, 38, 38);"> ，请你找出其中不含有重复字符的 </font><font style="color:rgb(38, 38, 38);">最长 </font>子串<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的长度。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
```

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        if n == 1:
            return 1
        left = 0
        window = set()
        window.add(s[left])
        res = 0
        for right in range(1, n):
            #如果出现重复，从左开始收缩窗口
            while s[right] in window:
                window.discard(s[left])
                left+=1

            #更新窗口长度
            temp = right-left+1
            res = max(res, temp)

            #没有重复时，右边扩张窗口
            window.add(s[right])
        return res
```

时间复杂度 O(N) ： 其中 N 为字符串长度，动态规划需遍历计算 dp 列表。

空间复杂度 O(1) ： 字符的 ASCII 码范围为 0 ~ 127 ，哈希表 dic 最多使用 O(128)=O(1) 大小的额外空间。



### 最长回文子串
动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，找到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中最长的 </font><font style="background-color:rgb(240, 240, 240);">回文</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">子串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：s = "cbbd"
输出："bb"
```

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        # 定义：dp[i][j]表示s[i]到s[j]是否为回文
        # 递推：dp[i][j]=dp[i+1][j-1]&(s[i]==s[j]) if j - i >= 2 else s[i]==s[j]
        dp = [[False]*n for i in range(n)]
        max_len = 0
        res = ""
        #i是左边界，从大到小   这样保证子串长度（j-i+1）是从小到大的，才能找到子串长度的最大值
        for i in range(n,-1,-1):
            #j是右边界，从小到大
            for j in range(i,n):
                #首尾是否相等
                if s[i] == s[j]:
                    #子串长度<=2
                    if j-i+1 <= 2:
                        dp[i][j] = True
                        if j-i+1 >max_len:
                            max_len = j-i+1
                            res = s[i:j+1]
                    #子串长度>2
                    elif dp[i+1][j-1]:
                        dp[i][j] = True
                        if j-i+1 >max_len:
                            max_len = j-i+1
                            res = s[i:j+1]

        return res
```

时间复杂度：O(n 2)，其中 n 是字符串的长度。动态规划的状态总数为 O(n2)，对于每个状态，我们需要转移的时间为 O(1)。

空间复杂度：O(n 2)，即存储动态规划状态需要的空间。



### [<font style="background-color:rgb(240, 240, 240);">最小覆盖子串（76）</font>](https://leetcode.cn/problems/minimum-window-substring/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 、一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中涵盖 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 所有字符的最小子串。如果 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中不存在涵盖 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 所有字符的子串，则返回空字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">""</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">对于</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中重复字符，我们寻找的子字符串中该字符数量必须不少于</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">t</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中该字符数量。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中存在这样的子串，我们保证它是唯一的答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
```

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        ans_left, ans_right = -1, len(s)
        cnt_s = Counter()  # s 子串字母的出现次数
        cnt_t = Counter(t)  # t 中字母的出现次数

        left = 0
        for right, c in enumerate(s):  # 移动子串右端点
            cnt_s[c] += 1  # 右端点字母移入子串
            while cnt_s >= cnt_t:  # 涵盖
                if right - left < ans_right - ans_left:  # 找到更短的子串
                    ans_left, ans_right = left, right  # 记录此时的左右端点
                cnt_s[s[left]] -= 1  # 左端点字母移出子串
                left += 1
        return "" if ans_left < 0 else s[ans_left: ans_right + 1]
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736229148391-f7c42354-bd52-415b-b046-9105ee3110d8.png)



# 三、链表
### 链表遍历
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def traverse_linked_list(head):
    current = head
    while current is not None:
        print(current.val)  # 打印当前节点的值
        current = current.next  # 移动到下一个节点

# 示例用法
if __name__ == "__main__":
    # 创建链表：1 -> 2 -> 3
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    
    node1.next = node2
    node2.next = node3
    
    # 遍历链表
    traverse_linked_list(node1)
```



### 两数相加
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非空</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的链表，表示两个非负的整数。它们每位数字都是按照 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">逆序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的方式存储的，并且每个节点只能存储 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一位</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 数字。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你将两个数相加，并以相同形式返回一个表示和的链表。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以假设除了数字 0 之外，这两个数都不会以 0 开头。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734611593209-8f409084-3601-4c1b-9959-91803e90c5a1.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        prenode = ListNode(0)
        lastnode = prenode
        val = 0
        while val or l1 or l2:
            val, cur = divmod(val + (l1.val if l1 else 0) + (l2.val if l2 else 0), 10)
            lastnode.next = ListNode(cur)
            lastnode = lastnode.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return prenode.next
```

### 删除链表倒数第N个节点
遍历/双指针

[https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表，删除链表的倒数第 </font>`<font style="color:rgba(38, 38, 38, 0.75);">n</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个结点，并且返回链表的头结点。</font>

```plain
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        def get_length(head):
          len = 0
          while head:
            len += 1
            head = head.next
          return len
          
        dummy = ListNode(0, head)
        len = get_length(head)
        cur = dummy
        #为了与题目中的 n 保持一致，节点的编号从 1 开始，头节点为编号 1 的节点。
        for i in range(1, len-n+1):
          cur = cur.next #遍历
        cur.next = cur.next.next #修改指针
        
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的长度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        left = dummy
        right = head
        #右指针先走N步
        for i in range(0, n):
            right = right.next

        #左右指针一起走，直到右指针走完
        while right:
            right = right.next
            left = left.next
        
        left.next = left.next.next
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的长度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



### 合并两个有序链表
迭代/递归

[https://leetcode.cn/problems/merge-two-sorted-lists/description/](https://leetcode.cn/problems/merge-two-sorted-lists/description/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">将两个升序链表合并为一个新的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">升序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 </font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735539752920-bc75a9ca-bc13-4530-8cc4-2892a2ce2cdd.jpeg)

```plain
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：l1 = [], l2 = []
输出：[]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        pre = ListNode(0)
        last = pre
        
        while list1 and list2:
          if list1.val < list2.val:
            last.next = ListNode(list1.val)
            list1 = list1.next
          else:
            last.next = ListNode(list2.val)
            list2 = list2.next
          last = last.next
        
        if list1:
          last.next = list1
        if list2:
          last.next = list2
          
        return pre.next
```

时间复杂度：O(n+m)，其中 n 和 m 分别为两个链表的长度。因为每次循环迭代中，l1 和 l2 只有一个元素会被放进合并链表中， 因此 while 循环的次数不会超过两个链表的长度之和。所有其他操作的时间复杂度都是常数级别的，因此总的时间复杂度为 O(n+m)。

空间复杂度：O(1)。我们只需要常数的空间存放若干变量。



### 合并K个升序链表
[https://leetcode.cn/problems/merge-k-sorted-lists/description/](https://leetcode.cn/problems/merge-k-sorted-lists/description/)

顺序合并/分治

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表数组，每个链表都已经按升序排列。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你将所有链表合并到一个升序链表中，返回合并后的链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：lists = []
输出：[]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
                pre = ListNode(0)
                last = pre
                
                while list1 and list2:
                    if list1.val < list2.val:
                        last.next = ListNode(list1.val)
                        list1 = list1.next
                    else:
                        last.next = ListNode(list2.val)
                        list2 = list2.next
                    last = last.next
                
                if list1:
                    last.next = list1
                if list2:
                    last.next = list2
                
                return pre.next
            
            pre = ListNode(-inf)
            for i in range(0, len(lists)):
                pre = mergeTwoLists(pre, lists[i])
            
            return pre.next
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735563502665-5ac3cd72-2dd4-4a2a-8fa9-028142073fa5.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564038789-78411734-6fac-45dc-9ab4-4c3b733b4d3e.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
                pre = ListNode(0)
                last = pre
                
                while list1 and list2:
                    if list1.val < list2.val:
                        last.next = ListNode(list1.val)
                        list1 = list1.next
                    else:
                        last.next = ListNode(list2.val)
                        list2 = list2.next
                    last = last.next
                
                if list1:
                    last.next = list1
                if list2:
                    last.next = list2
                
                return pre.next
            
            #递归实现分治
            def merge(lists, l, r):
                if l == r : return lists[l]
                if l > r : return None
                mid = (l + r) // 2
                return mergeTwoLists(merge(lists, l, mid), merge(lists, mid+1, r))
            
            return merge(lists, 0, len(lists)-1)
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564021238-2891c512-2052-4a36-ab8a-a49fc8a89284.png)



### 两两交换链表中的节点
[https://leetcode.cn/problems/swap-nodes-in-pairs/description/](https://leetcode.cn/problems/swap-nodes-in-pairs/description/)

<font style="background-color:rgb(240, 240, 240);">迭代/递归</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735564809704-6ff2befb-3fb7-4be2-804b-35f783dbe4e3.jpeg)

```plain
输入：head = [1,2,3,4]
输出：[2,1,4,3]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：head = []
输出：[]
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564702800-b52a7e12-6fdc-4133-8787-a10a1062084a.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564719963-af49ae7c-35ff-4e79-a121-3c79dec2158b.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        tmp = dummy
        
        while tmp.next and tmp.next.next:
            node1 = tmp.next
            node2 = tmp.next.next

            # 图1 交换两个节点
            tmp.next = node2
            node1.next = node2.next
            node2.next = node1

            # 图2向前移动两步（此时node1已经交换完毕）
            tmp = node1
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的节点数量。需要对每个节点进行更新指针的操作。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

### 反转链表
[https://leetcode.cn/problems/reverse-linked-list/description/](https://leetcode.cn/problems/reverse-linked-list/description/)

迭代（双指针）/递归

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你反转链表，并返回反转后的链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735565333487-67798235-83d4-4a74-94b2-e26cb074c84a.jpeg)

```plain
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            #暂存后继节点
            tmp = cur.next
            #修改当前节点指针
            cur.next = pre
            #双指针向前移动
            pre = cur
            cur = tmp
        return pre
```

+ **<font style="background-color:rgb(240, 240, 240);">时间复杂度</font>****<font style="background-color:rgb(240, 240, 240);"> </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>****<font style="background-color:rgb(240, 240, 240);"> </font>****<font style="background-color:rgb(240, 240, 240);">：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">遍历链表使用线性大小时间。</font>
+ **<font style="background-color:rgb(240, 240, 240);">空间复杂度 </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font>****<font style="background-color:rgb(240, 240, 240);"> ：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 变量 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pre</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">cur</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 使用常数大小额外空间</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">K 个一组翻转链表</font>](https://leetcode.cn/problems/reverse-nodes-in-k-group/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你链表的头节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，每 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个节点一组进行翻转，请你返回修改后的链表。</font>

`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的整数倍，那么请将最后剩余的节点保持原有顺序。你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735566315916-95e64509-b54f-423c-82f5-6729b1f9fbba.jpeg)

```plain
输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566153716-13813087-2db6-4c0a-be08-bbb21ddd92b3.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566263872-b13f068d-6761-42b6-8f19-6c139a47fb0b.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
            def reverseList(head, tail):
                pre = tail.next
                cur = head
                while pre != tail:
                    #暂存后继节点
                    tmp = cur.next
                    #修改当前节点指针
                    cur.next = pre
                    #双指针向前移动
                    pre = cur
                    cur = tmp
                return tail, head
            
            dummy = ListNode(0)
            dummy.next = head
            pre = dummy

            while head:
                tail = pre

                #step1 图1 tail指针先走K步，如果走不到k步则说明已经反转完成
                for i in range(k):
                    tail = tail.next
                    if not tail:
                        return dummy.next
                
                #step2 图1 记录nex节点位置
                nex = tail.next

                #step3 图1 反转k个节点
                head, tail = reverseList(head, tail)

                #step4 图2 把子链表接回原链表
                pre.next = head
                tail.next = nex

                #step5 图2 移动pre head指针
                pre = tail
                head = tail.next
            
            return dummy.next
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566382698-9390a2cc-e3c5-4b53-ba07-85f3f900e157.png)



### [<font style="background-color:rgb(240, 240, 240);">环形链表（141）</font>](https://leetcode.cn/problems/linked-list-cycle/)
双指针  哈希表

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表的头节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，判断链表中是否有环。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中有某个节点，可以通过连续跟踪</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">next</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">来表示链表尾连接到链表中的位置（索引从 0 开始）。</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>**`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不作为参数进行传递 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。仅仅是为了标识链表的实际情况。</font>

_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中存在环</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，则返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。 否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736404645268-bfbdc8d2-16dc-4363-aea9-5a6ae7c8c648.png)

```plain
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        #快慢指针
        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            #如果相遇  说明有环
            if slow == fast:
                return True
        
        return False
```

时间复杂度：O(N)，其中 N 是链表中的节点数。

当链表中不存在环时，快指针将先于慢指针到达链表尾部，链表中每个节点至多被访问两次。

当链表中存在环时，每一轮移动后，快慢指针的距离将减小一。初始距离为环的长度，因此至多移动 N 轮。

空间复杂度：O(1)。我们只使用了两个指针的额外空间。







### [<font style="background-color:rgb(240, 240, 240);">环形链表 II（142）</font>](https://leetcode.cn/problems/linked-list-cycle-ii/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个链表的头节点  </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回链表开始入环的第一个节点。 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表无环，则返回 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">null</font>_`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>_

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中有某个节点，可以通过连续跟踪</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">next</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">来表示链表尾连接到链表中的位置（</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">索引从 0 开始</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）。如果</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，则在该链表中没有环。</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>**`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不作为参数进行传递</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，仅仅是为了标识链表的实际情况。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不允许修改 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。
```

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        flag = 0
        while slow and fast and fast.next:
            if not (fast and fast.next): return
            slow = slow.next
            fast = fast.next.next
            #快慢指针相遇
            if slow == fast :
                #有环标记
                flag = 1 
                break

        if flag == 0:
            return None
        
        ptr = head
        while ptr != slow:
            #有了 a=c+(n−1)(b+c) 的等量关系，我们会发现：从相遇点到入环点的距离加上 n−1 圈的环长，恰好等于从链表头部到入环点的距离。
            # 因此，当发现 slow 与 fast 相遇时，我们再额外使用一个指针 ptr。起始，它指向链表头部；随后，它和 slow 每次向后移动一个位置。最终，它们会在入环点相遇。
            #第3指针和慢指针相遇点，就是入环点
            ptr = ptr.next
            slow = slow.next
        return ptr
```

时间复杂度 O(N) ：第二次相遇中，慢指针须走步数 a<a+b；第一次相遇中，慢指针须走步数 a+b−x<a+b，其中 x 为双指针重合点与环入口距离；因此总体为线性复杂度；

空间复杂度 O(1) ：双指针使用常数大小的额外空间。

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        hashmap = set()
        
        cur = head
        while cur:
            if cur in hashmap:
                return cur
            hashmap.add(cur)
            cur = cur.next
        
        return None
```

时间复杂度：O(N)，其中 N 为链表中节点的数目。我们恰好需要访问链表中的每一个节点。

空间复杂度：O(N)，其中 N 为链表中节点的数目。我们需要将链表中的每个节点都保存在哈希表当中。





### [<font style="background-color:rgb(240, 240, 240);">排序链表（148）</font>](https://leetcode.cn/problems/sort-list/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你链表的头结点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请将其按 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">升序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 排列并返回 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">排序后的链表</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736407916227-6d72d866-c30c-48d5-8515-0e652ab8e885.jpeg)

```plain
输入：head = [4,2,1,3]
输出：[1,2,3,4]
```



方法一：归并排序（分治）

找到链表的中间结点 head 2的前一个节点，并断开 head 2与其前一个节点的连接。这样我们就把原链表均分成了两段更短的链表。原理见【基础算法精讲 07】。

分治，递归调用 sortList，分别排序 head（只有前一半）和 head 2 。

排序后，我们得到了两个有序链表，那么合并两个有序链表，得到排序后的链表，返回链表头节点。原理见 我的题解。

```python
class Solution:
    # 876. 链表的中间结点（快慢指针）
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        # 先找到链表的中间结点的【前一个节点】
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next  # 下一个节点就是链表的中间结点 mid
        slow.next = None  # 断开 mid 的前一个节点和 mid 的连接
        return mid

    # 21. 合并两个有序链表（双指针）
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 用哨兵节点简化代码逻辑
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1  # 把 list1 加到新链表中
                list1 = list1.next
            else:  # 注：相等的情况加哪个节点都是可以的
                cur.next = list2  # 把 list2 加到新链表中
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2  # 拼接剩余链表
        return dummy.next

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 如果链表为空或者只有一个节点，无需排序
        if head is None or head.next is None:
            return head
        # 找到中间节点，并断开 head2 与其前一个节点的连接
        # 比如 head=[4,2,1,3]，那么 middleNode 调用结束后 head=[4,2] head2=[1,3]
        head2 = self.middleNode(head)
        # 分治
        head = self.sortList(head)
        head2 = self.sortList(head2)
        # 合并
        return self.mergeTwoLists(head, head2)
```

时间复杂度：O(nlogn)，其中 n 是链表长度。递归式 T(n)=2T(n/2)+O(n)，由主定理可得时间复杂度为 O(nlogn)。

空间复杂度：O(logn)。递归需要 O(logn) 的栈开销。





### [相交链表（160）](https://leetcode.cn/problems/intersection-of-two-linked-lists/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">headA</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">headB</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">null</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">图示两个链表在节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">c1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">开始相交</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736413742352-0baf7dc6-4c02-4ccb-b1c9-dec0edeeb702.png)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">题目数据</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保证</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整个链式结构中不存在环。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，函数返回结果后，链表必须 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保持其原始结构</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
            
        #哈希表
        node_set = set()
        ptr_a, ptr_b = headA, headB
        #先遍历a
        while ptr_a:
            node_set.add(ptr_a)
            ptr_a = ptr_a.next
        #再遍历b
        while ptr_b:
            if ptr_b in node_set:
                return ptr_b
            ptr_b = ptr_b.next
        
        return None
```

时间复杂度：O(m+n)，其中 m 和 n 是分别是链表 headA 和 headB 的长度。需要遍历两个链表各一次。

空间复杂度：O(m)，其中 m 是链表 headA 的长度。需要使用哈希集合存储链表 headA 中的全部节点。

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
            
        node_set = set()
        ptr_a, ptr_b = headA, headB
        #当指针 pA 和 pB 指向同一个节点或者都为空时，返回它们指向的节点或者 null
        while ptr_a != ptr_b:
            #如果指针 pA 不为空，则将指针 pA 移到下一个节点  如果指针 pA 为空，则将指针 pA 移到链表 headB 的头节点
            ptr_a = ptr_a.next if ptr_a != None else headB
            #pB操作相同
            ptr_b = ptr_b.next if ptr_b != None else headA
        return ptr_a
            
```

时间复杂度：O(m+n)，其中 m 和 n 是分别是链表 headA 和 headB 的长度。两个指针同时遍历两个链表，每个指针遍历两个链表各一次。

空间复杂度：O(1)。



### [<font style="background-color:rgb(240, 240, 240);"> 回文链表（234）</font>](https://leetcode.cn/problems/palindrome-linked-list/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你判断该链表是否为</font><font style="background-color:rgb(240, 240, 240);">回文链表</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果是，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736491482814-b1f516d7-c19a-4d7f-bbc1-023d2a76191a.jpeg)

```plain
输入：head = [1,2,2,1]
输出：true
```

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        def reverse_list(node):
            pre = None
            cur = node
            while cur:
                #暂存后继节点
                tmp = cur.next
                #修改当前节点指针
                cur.next = pre
                #双指针向前移动
                pre = cur
                cur = tmp
            return pre

        def find_middle_node(node):
            slow, fast = node, node
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            return slow
        
        if not head:
            return False

        
        #找到中间节点
        first_half_end = find_middle_node(head)
        
        #反转链表后一半
        second_half_start = reverse_list(first_half_end)
        
        #判断前一半和后一半的反转是否一致
        n1, n2 = head, second_half_start
        while n1 and n2:
            if n1.val != n2.val:
                return False
            n1 = n1.next
            n2 = n2.next
        
        #恢复链表后一半    
        first_half_end.next = reverse_list(second_half_start)
        
        return True
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">指的是链表的大小。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。我们只会修改原本链表中节点的指向，而在堆栈上的堆栈帧不超过 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        def reverse_list(node):
            pre = None
            cur = node
            while cur:
                #暂存后继节点
                tmp = cur.next
                #修改当前节点指针
                cur.next = pre
                #双指针向前移动
                pre = cur
                cur = tmp
            return pre

        
        head2 = reverse_list(copy.deepcopy(head))
        
        n1, n2 = head, head2
        while n1 and n2:
            if n1.val != n2.val:
                return False
            n1 = n1.next
            n2 = n2.next
        return True
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指的是链表的大小。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 指的是链表的大小。</font>

# <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">四、二叉树</font>
### <font style="color:rgb(51, 51, 51);">二叉树遍历</font>
+ 广度优先搜索可以按照层次的顺序从上到下遍历所有的节点
+ 深度优先搜索可以从一个根开始，一直延伸到某个叶，然后回到根，到达另一个分支。根据根节点、左节点和右节点之间的相对顺序，可以进一步将深度优先搜索策略区分为：
    - <font style="color:rgb(51, 51, 51);">前序遍历：根 -> 左 -> 右</font>
    - <font style="color:rgb(51, 51, 51);">中序遍历：左 -> 根 -> 右</font>
    - <font style="color:rgb(51, 51, 51);">后序遍历：左 -> 右 -> 根</font>

#### <font style="color:rgb(51, 51, 51);">1. 前序遍历（Pre-order Traversal）</font>
<font style="color:rgb(51, 51, 51);">前序遍历的顺序是：</font>

1. <font style="color:rgb(51, 51, 51);">访问根节点</font>
2. <font style="color:rgb(51, 51, 51);">遍历左子树</font>
3. <font style="color:rgb(51, 51, 51);">遍历右子树</font>

<font style="color:rgb(51, 51, 51);">具体实现时，一般可以使用递归或栈来完成。前序遍历的优点是可以很方便地复制整个树或创建树的表示。</font>

**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
      A
     / \
    B   C
   / \
  D   E
```

<font style="color:rgb(51, 51, 51);">前序遍历的结果为：A, B, D, E, C</font>

#### <font style="color:rgb(51, 51, 51);">2. 中序遍历（In-order Traversal）</font>
<font style="color:rgb(51, 51, 51);">中序遍历的顺序是：</font>

1. <font style="color:rgb(51, 51, 51);">遍历左子树</font>
2. <font style="color:rgb(51, 51, 51);">访问根节点</font>
3. <font style="color:rgb(51, 51, 51);">遍历右子树</font>

<font style="color:rgb(51, 51, 51);">中序遍历的特点是对于二叉搜索树（BST），遍历结果将是一个有序的序列（从小到大）。</font>

**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
      A
     / \
    B   C
   / \
  D   E
```

<font style="color:rgb(51, 51, 51);">中序遍历的结果为：D, B, E, A, C</font>

#### <font style="color:rgb(51, 51, 51);">3. 后序遍历（Post-order Traversal）</font>
<font style="color:rgb(51, 51, 51);">后序遍历的顺序是：</font>

1. <font style="color:rgb(51, 51, 51);">遍历左子树</font>
2. <font style="color:rgb(51, 51, 51);">遍历右子树</font>
3. <font style="color:rgb(51, 51, 51);">访问根节点</font>

<font style="color:rgb(51, 51, 51);">后序遍历常用于计算节点的深度、删除树节点等操作。</font>

**<font style="color:rgb(51, 51, 51);">示例</font>**<font style="color:rgb(51, 51, 51);">：</font>

```plain
      A
     / \
    B   C
   / \
  D   E
```

<font style="color:rgb(51, 51, 51);">后序遍历的结果为：D, E, B, C, A</font>



### 二叉搜索树
<font style="color:rgb(51, 51, 51);">二叉搜索树（Binary Search Tree，简称 BST）是一种数据结构，用于存储有序的数据。它具有以下性质：</font>

1. **<font style="color:rgb(51, 51, 51);">节点结构</font>**<font style="color:rgb(51, 51, 51);">：每个节点包含一个键（值）、一个指向左子树的指针和一个指向右子树的指针。</font>
2. **<font style="color:rgb(51, 51, 51);">左小右大</font>**<font style="color:rgb(51, 51, 51);">：对于任意一个节点，</font><font style="color:#DF2A3F;">左子树上的所有节点的键值都小于该节点的键值，右子树上的所有节点的键值都大于该节点的键值。</font>
3. **<font style="color:rgb(51, 51, 51);">无重复</font>**<font style="color:rgb(51, 51, 51);">：通常，二叉搜索树不允许有重复的键值。</font>

<font style="color:rgb(51, 51, 51);">二叉搜索树的常见操作包括：</font>

+ **<font style="color:rgb(51, 51, 51);">插入</font>**<font style="color:rgb(51, 51, 51);">：根据键值的大小，将新节点插入到适当的位置。</font>
+ **<font style="color:rgb(51, 51, 51);">查找</font>**<font style="color:rgb(51, 51, 51);">：通过比较键值，定位到想要查找的节点。</font>
+ **<font style="color:rgb(51, 51, 51);">删除</font>**<font style="color:rgb(51, 51, 51);">：删除给定键值的节点。删除的过程较复杂，需要处理三个情况：</font>
    - <font style="color:rgb(51, 51, 51);">被删除节点是叶子节点（没有子节点）。</font>
    - <font style="color:rgb(51, 51, 51);">被删除节点只有一个子节点。</font>
    - <font style="color:rgb(51, 51, 51);">被删除节点有两个子节点（通常需要找到其右子树中的最小值或左子树中的最大值来替代）。</font>
+ **<font style="color:rgb(51, 51, 51);">遍历</font>**<font style="color:rgb(51, 51, 51);">：可以使用中序遍历、前序遍历或后序遍历来访问树中的所有节点。中序遍历会返回一个有序的键值序列。</font>

<font style="color:rgb(51, 51, 51);">二叉搜索树的时间复杂度（理想情况）：</font>

+ <font style="color:rgb(51, 51, 51);">查找、插入和删除操作的时间复杂度为 O(log n)，其中 n 是树中的节点数。  
</font><font style="color:rgb(51, 51, 51);">然而，如果树不是平衡的，时间复杂度可能会退化为 O(n)，比如在插入顺序为递增或递减的情况下。因此，为了保持较好的性能，常常使用平衡树（如红黑树、AVL树等）来代替普通的二叉搜索树。</font>
+ <font style="color:rgb(51, 51, 51);"></font>

### [二叉树的中序遍历（94）](https://leetcode.cn/problems/binary-tree-inorder-traversal/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个二叉树的根节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">它的 </font>__**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中序</font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 遍历</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736235346232-32164de9-4c5e-41b5-b4d7-8cd091e433ca.jpeg)

```plain
输入：root = [1,null,2,3]
输出：[1,3,2]
```

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def inorder(node):
            nonlocal res
            if not node:
                return
            
            #中序遍历
            inorder(node.left)
            res.append(node.val)
            inorder(node.right)
            
            # #前序遍历
            # res.append(node.val)
            # inorder(node.left)
            # inorder(node.right)
            
            # #后序遍历
            # inorder(node.left)
            # inorder(node.right)
            # res.append(node.val)
        
        res = []
        inorder(root)
        return res
```

<font style="color:rgb(51, 51, 51);">时间复杂度：O(n)，其中 n 为二叉树节点的个数。二叉树的遍历中每个节点会被访问一次且只会被访问一次。</font>

<font style="color:rgb(51, 51, 51);">空间复杂度：O(n)。空间复杂度取决于递归的栈深度，而栈深度在二叉树为一条链的情况下会达到 O(n) 的级别。</font>

```python
class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        WHITE, GRAY = 0, 1
        res = []
        #使用颜色标记节点的状态，新节点为白色，已访问的节点为灰色。
        stack = [(WHITE, root)]
        while stack:
            color, node = stack.pop()
            if node is None: continue
            #如果遇到的节点为白色，则将其标记为灰色，然后将其右子节点、自身、左子节点依次入栈。
            if color == WHITE:
                stack.append((WHITE, node.right))
                stack.append((GRAY, node))
                stack.append((WHITE, node.left))
            #如果遇到的节点为灰色，则将节点的值输出。
            else:
                res.append(node.val)
        return res

```

时间复杂度：O(n)，其中 n 为二叉树节点的个数。二叉树的遍历中每个节点会被访问一次且只会被访问一次。

空间复杂度：O(n)。空间复杂度取决于栈深度，而栈深度在二叉树为一条链的情况下会达到 O(n) 的级别。



### [<font style="background-color:rgb(240, 240, 240);">不同的二叉搜索树（96）</font>](https://leetcode.cn/problems/unique-binary-search-trees/)
**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736237513103-6afde88d-9f2a-4c1e-84b4-e416b52949bc.jpeg)

```plain
输入：n = 3
输出：5
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：n = 1
输出：1
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736237544926-73c3be96-737f-474e-ac6a-9981b54a4c20.png)

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736237690007-32089678-84d5-41d1-8131-bc52f9e183e8.png)

```python
class Solution:
    def numTrees(self, n):
        """
        :type n: int
        :rtype: int
        """
        G = [0]*(n+1)
        G[0], G[1] = 1, 1
        # G(n): 长度为 n 的序列能构成的不同二叉搜索树的个数。
        # F(i,n): 以 i 为根、序列长度为 n 的不同二叉搜索树个数 (1≤i≤n)。

        for i in range(2, n+1):
            for j in range(1, i+1):
                #左序列构建左子树的数量为G(i-1), 右序列构建左子树的数量为G(n-i)
                #选择数字 i 作为根，则根为 i 的所有二叉搜索树的集合是左子树集合和右子树集合的笛卡尔积 F(i,n)=G(i−1)⋅G(n−i)  
                G[i] += G[j-1] * G[i-j]

        return G[n]
```

时间复杂度 : O(n ^2)，其中 n 表示二叉搜索树的节点个数。G(n) 函数一共有 n 个值需要求解，每次求解需要 O(n) 的时间复杂度，因此总时间复杂度为 O(n ^2 )。

空间复杂度 : O(n)。我们需要 O(n) 的空间存储 G 数组。



### [不同的二叉搜索树 II（95）](https://leetcode.cn/problems/unique-binary-search-trees-ii/)
给你一个整数 `<font style="color:rgba(38, 38, 38, 0.75);">n</font>` ，请你生成并返回所有由 `<font style="color:rgba(38, 38, 38, 0.75);">n</font>` 个节点组成且节点值从 `<font style="color:rgba(38, 38, 38, 0.75);">1</font>` 到 `<font style="color:rgba(38, 38, 38, 0.75);">n</font>` 互不相同的不同 **二叉搜索树**_ _。可以按 **任意顺序** 返回答案。

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736239489033-34b4f22b-c154-44ef-a422-1ec3f3256dd7.jpeg)

```plain
输入：n = 3
输出：[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：n = 1
输出：[[1]]
```

```python
class Solution:
    def generateTrees(self, n: int) -> List[TreeNode]:
        def generateTrees(start, end):
            if start > end:
                return [None,]
            
            allTrees = []
            for i in range(start, end + 1):  # 枚举可行根节点
                # 获得所有可行的左子树集合
                leftTrees = generateTrees(start, i - 1)
                
                # 获得所有可行的右子树集合
                rightTrees = generateTrees(i + 1, end)
                
                # 从左子树集合中选出一棵左子树，从右子树集合中选出一棵右子树，拼接到根节点上
                for l in leftTrees:
                    for r in rightTrees:
                        currTree = TreeNode(i)
                        currTree.left = l
                        currTree.right = r
                        allTrees.append(currTree)
            
            return allTrees
        
        return generateTrees(1, n) if n else []

```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736239479010-a4c0e846-a6e2-4719-bc7b-d1ed4df45225.png)





### [<font style="background-color:rgb(240, 240, 240);">验证二叉搜索树（98）</font>](https://leetcode.cn/problems/validate-binary-search-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个二叉树的根节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，判断其是否是一个有效的二叉搜索树。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">有效</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">二叉搜索树定义如下：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点的左</font><font style="background-color:rgb(240, 240, 240);">子树</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">只包含</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">小于</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">当前节点的数。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点的右子树只包含</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">大于</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">当前节点的数。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">所有左子树和右子树自身必须也是二叉搜索树。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736241206165-916110f1-627b-42b8-abd1-f7c2fe4a53c0.jpeg)

```plain
输入：root = [2,1,3]
输出：true
```

```python
class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def helper(node, lower = float('-inf'), upper = float('inf')) -> bool:
            if not node:
                return True
            
            val = node.val
            #不满足二叉搜索树的性质
            if val <= lower or val >= upper:
                return False

            #递归调用右子树时，我们需要把下界 lower 改为 root.val
            if not helper(node.right, val, upper):
                return False
            #在递归调用左子树时，我们需要把上界 upper 改为 root.val
            if not helper(node.left, lower, val):
                return False
            return True

        return helper(root)
```

时间复杂度：O(n)，其中 n 为二叉树的节点个数。在递归调用的时候二叉树的每个节点最多被访问一次，因此时间复杂度为 O(n)。

空间复杂度：O(n)，其中 n 为二叉树的节点个数。递归函数在递归过程中需要为每一层递归函数分配栈空间，所以这里需要额外的空间且该空间取决于递归的深度，即二叉树的高度。最坏情况下二叉树为一条链，树的高度为 n ，递归最深达到 n 层，故最坏情况下空间复杂度为 O(n) 。



### [<font style="background-color:rgb(240, 240, 240);">对称二叉树（101）</font>](https://leetcode.cn/problems/symmetric-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个二叉树的根节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ， 检查它是否轴对称。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736242645615-241364de-0ca3-4823-9ef5-e46f17aedd7a.png)

```plain
输入：root = [1,2,2,3,4,4,3]
输出：true
```

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def check(p, q):
            #两个节点均为空
            if p == None and q == None:
                return True
            #有一个是空
            if p == None or q == None:
                return False
            #值不相同
            if p.val != q.val:
                return False
            
            return check(p.left, q.right) and check(p.right, q.left)
        
        return check(root.left, root.right)
```

假设树上一共 n 个节点。

时间复杂度：这里遍历了这棵树，渐进时间复杂度为 O(n)。

空间复杂度：这里的空间复杂度和递归使用的栈空间有关，这里递归层数不超过 n，故渐进空间复杂度为 O(n)。



### [<font style="background-color:rgb(240, 240, 240);">二叉树的层序遍历（102）</font>](https://leetcode.cn/problems/binary-tree-level-order-traversal/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你二叉树的根节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回其节点值的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">层序遍历</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。 （即逐层地，从左到右访问所有节点）。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736249618904-426a3dba-5ecf-48f0-beac-438993b6815e.jpeg)

```plain
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root : return []
        res = []
        queue = [root]
        #BFS
        while len(queue) > 0:
            tmp = [] #新建一个临时列表 tmp ，用于存储当前层打印结果。
            #当前层打印循环： 循环次数为当前层节点数（即队列 queue 长度）。
            for i in range(len(queue)):
                node = queue.pop(0) #出队： 队首元素出队，记为 node。
                tmp.append(node.val) # 打印： 将 node.val 添加至 tmp 尾部。
                #添加子节点： 若 node 的左（右）子节点不为空，则将左（右）子节点加入队列 queue 。
                if node.left : queue.append(node.left)
                if node.right : queue.append(node.right)
            #将当前层结果 tmp 添加入 res 
            res.append(tmp)
        return res
```

时间复杂度 O(N) ： N 为二叉树的节点数量，即 BFS 需循环 N 次。

空间复杂度 O(N) ： 最差情况下，即当树为平衡二叉树时，最多有 N/2 个树节点同时在 queue 中，使用 O(N) 大小的额外空间。



### [<font style="background-color:rgb(240, 240, 240);">二叉树的最大深度（104）</font>](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个二叉树</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回其最大深度。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">二叉树的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最大深度</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是指从根节点到最远叶子节点的最长路径上的节点数。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736249990459-cde3284a-9d3d-4926-a51e-e169bc730f2e.jpeg)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

```plain
输入：root = [3,9,20,null,null,15,7]
输出：3
```

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def inorder(node, depth):
            nonlocal max_depth
            if not node:
                max_depth = max(max_depth, depth)
                return
            
            #中序遍历
            inorder(node.left, depth+1)
            # res.append(node.val)
            inorder(node.right, depth+1)
        
        max_depth = 0
        inorder(root, 0)
        return max_depth
        
```

<font style="color:rgb(51, 51, 51);">时间复杂度：O(n)，其中 n 为二叉树节点的个数。二叉树的遍历中每个节点会被访问一次且只会被访问一次。</font>

<font style="color:rgb(51, 51, 51);">空间复杂度：O(n)。空间复杂度取决于递归的栈深度，而栈深度在二叉树为一条链的情况下会达到 O(n) 的级别。</font>

<font style="color:rgb(51, 51, 51);"></font>

### [<font style="background-color:rgb(240, 240, 240);">从前序与中序遍历序列构造二叉树（105）</font>](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定两个整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">preorder</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">inorder</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">preorder</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是二叉树的</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">先序遍历</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">， </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">inorder</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是同一棵树的</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中序遍历</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请构造二叉树并返回其根节点。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
输出: [3,9,20,null,null,15,7]
```

```python
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # 对于任意一颗树而言，前序遍历的形式总是
        # [ 根节点, [左子树的前序遍历结果], [右子树的前序遍历结果] ]
        # 中序遍历的形式总是
        # [ [左子树的中序遍历结果], 根节点, [右子树的中序遍历结果] ]
        def my_build_tree(preorder, inorder):
            if not preorder:
                return None
            node = TreeNode(preorder[0])# preorder[0]是根节点
            idx = inorder.index(preorder[0]) #根据根节点和中序遍历，找到左右子树

            node.left = my_build_tree(preorder[1:idx+1], inorder[:idx])
            node.right = my_build_tree(preorder[idx+1:], inorder[idx+1:])
            return node
            
        return my_build_tree(preorder, inorder)
```

时间复杂度：O(n)，其中 n 是树中的节点个数。

空间复杂度：O(n)，除去返回的答案需要的 O(n) 空间之外，我们还需要使用 O(n) 的空间存储哈希映射，以及 O(h)（其中 h 是树的高度）的空间表示递归时栈空间。这里 h<n，所以总空间复杂度为 O(n)。





### [<font style="background-color:rgb(240, 240, 240);">二叉树展开为链表（114）</font>](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你二叉树的根结点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你将它展开为一个单链表：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">展开后的单链表应该同样使用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">TreeNode</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">right</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">子指针指向链表中下一个结点，而左子指针始终为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">null</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">展开后的单链表应该与二叉树 </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">先序遍历</font>](https://baike.baidu.com/item/%E5%85%88%E5%BA%8F%E9%81%8D%E5%8E%86/6442839?fr=aladdin)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 顺序相同。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：root = [1,2,5,3,4,null,6]
输出：[1,null,2,null,3,null,4,null,5,null,6]
```

```python
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        def inorder(node):
            if not node:
                return
            
            # #前序遍历
            res.append(node)
            inorder(node.left)
            inorder(node.right)

        res = []
        inorder(root)
        
        if len(res) == 0:
            return []

        #遍历前序遍历的结果
        for i in range(len(res)-1):
            res[i].left = None
            res[i].right = res[i+1]
        
        return res[0]
```

时间复杂度：O(n)，其中 n 是二叉树的节点数。前序遍历的时间复杂度是 O(n)，前序遍历之后，需要对每个节点更新左右子节点的信息，时间复杂度也是 O(n)。

空间复杂度：O(n)，其中 n 是二叉树的节点数。空间复杂度取决于栈（递归调用栈或者迭代中显性使用的栈）和存储前序遍历结果的列表的大小，栈内的元素个数不会超过 n，前序遍历列表中的元素个数是 n。





### [<font style="background-color:rgb(240, 240, 240);">二叉树中的最大路径和（124）</font>](https://leetcode.cn/problems/binary-tree-maximum-path-sum/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">二叉树中的</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">路径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">至多出现一次</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。该路径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">至少包含一个</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点，且不一定经过根节点。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">路径和</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是路径中各节点值的总和。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个二叉树的根节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回其 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最大路径和</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：root = [1,2,3]
输出：6
解释：最优路径是 2 -> 1 -> 3 ，路径和为 2 + 1 + 3 = 6
```

```python
class Solution:
    def __init__(self):
        #全局变量 记录最大值
        self.maxSum = float("-inf")
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        #递归函数，计算当前节点的最大贡献值
        def my_max_gain(node):
            if not node:
                return 0
            
            #计算左/右子树的增益
            left_gain = max(my_max_gain(node.left), 0)
            right_gain = max(my_max_gain(node.right), 0)
            
            #当前节点的最大路径值
            node_path = node.val + left_gain + right_gain
            
            #更新最大值
            self.maxSum = max(self.maxSum, node_path)
            
            #返回当前节点的最大贡献
            return node.val + max(left_gain, right_gain)
        
        my_max_gain(root)    
        
        return self.maxSum
```

时间复杂度：O(N)，其中 N 是二叉树中的节点个数。对每个节点访问不超过 2 次。

空间复杂度：O(N)，其中 N 是二叉树中的节点个数。空间复杂度主要取决于递归调用层数，最大层数等于二叉树的高度，最坏情况下，二叉树的高度等于二叉树中的节点个数。



### [翻转二叉树（226）](https://leetcode.cn/problems/invert-binary-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一棵二叉树的根节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，翻转这棵二叉树，并返回其根节点。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736480718710-7a244c1f-c09e-4597-a9e2-428592f2fb0a.jpeg)

```plain
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def reverse_tree(node):
            if not node:
                return
            
            #反转当前node
            tmp_node = node.left
            node.left = node.right
            node.right = tmp_node
            
            #递归
            reverse_tree(node.left)
            reverse_tree(node.right)
        
        reverse_tree(root)
        return root
```

时间复杂度：O(N)，其中 N 为二叉树节点的数目。我们会遍历二叉树中的每一个节点，对每个节点而言，我们在常数时间内交换其两棵子树。

空间复杂度：O(N)。使用的空间由递归栈的深度决定，它等于当前节点在二叉树中的高度。在平均情况下，二叉树的高度与节点个数为对数关系，即 O(logN)。而在最坏情况下，树形成链状，空间复杂度为 O(N)。





### [ 二叉树的最近公共祖先（236）](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。</font>

[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">百度百科</font>](https://baike.baidu.com/item/%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88/8918834?fr=aladdin)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一个节点也可以是它自己的祖先</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）。”</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736492541103-fdfb0bff-4ed2-4c2b-a077-694356ec8c70.png)

```plain
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3 。
```

```python
class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        #考虑通过递归对二叉树进行先序遍历，当遇到节点 p 或 q 时返回。从底至顶回溯，当节点 p,q 在节点 root 的异侧时，节点 root 即为最近公共祖先，则向上返回 root 。
        #当 root 等于 p,q ，则直接返回 root ；
        if not root or root == p or root == q: return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        #当 left 和 right 同时为空 ：说明 root 的左 / 右子树中都不包含 p,q ，返回 null ；
        if not left and not right: return # 1.
        # 当 left 为空 ，right 不为空 ：p,q 都不在 root 的左子树中，直接返回 right 。具体可分为两种情况：
            # p,q 其中一个在 root 的 右子树 中，此时 right 指向 p（假设为 p ）；
            # p,q 两节点都在 root 的 右子树 中，此时的 right 指向 最近公共祖先节点 ；
        if not left: return right # 3.
        if not right: return left # 4.
        #当 left 和 right 同时不为空 ：说明 p,q 分列在 root 的 异侧 （分别在 左 / 右子树），因此 root 为最近公共祖先，返回 root ；
        return root # 2. if left and right:
```

时间复杂度 O(N) ： 其中 N 为二叉树节点数；最差情况下，需要递归遍历树的所有节点。

空间复杂度 O(N) ： 最差情况下，递归深度达到 N ，系统使用 O(N) 大小的额外空间。



### [<font style="background-color:rgb(240, 240, 240);">二叉树的序列化与反序列化（297）</font>](https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/)（DFS）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">序列化是将一个数据结构或者对象转换为连续的比特位的操作，进而可以将转换后的数据存储在一个文件或者内存中，同时也可以通过网络传输到另一个计算机环境，采取相反方式重构得到原数据。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请设计一个算法来实现二叉树的序列化与反序列化。这里不限定你的序列 / 反序列化算法执行逻辑，你只需要保证一个二叉树可以被序列化为一个字符串并且将这个字符串反序列化为原始的树结构。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">提示: </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">输入输出格式与 LeetCode 目前使用的方式一致，详情请参阅 </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">LeetCode 序列化二叉树的格式</font>](https://support.leetcode.cn/hc/kb/article/1567641/)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。你并非必须采取这种方式，你也可以采用其他的方法解决这个问题。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736740842320-4ce90112-a2d3-415d-8236-d82d47cf452f.jpeg)

```plain
输入：root = [1,2,3,null,null,4,5]
输出：[1,2,3,null,null,4,5]
```

```python
class Codec:
    def serialize(self, root):
        res = []
        def dfs(root):
            if not root:
                res.append('#')
                return
            res.append(str(root.val)) # 必须将 int 转化为 str
            dfs(root.left)
            dfs(root.right)
        dfs(root)
        return ','.join(res)

    def deserialize(self, data):
        lst = data.split(',')
        def dfs():
            if not lst:
                return
            val = lst.pop(0)
            if val=='#':
                return
            root = TreeNode(int(val))
            root.left = dfs()
            root.right = dfs()
            return root
        return dfs()
```

时间复杂度：在序列化和反序列化函数中，我们只访问每个节点一次，因此时间复杂度为 O(n)，其中 n 是节点数，即树的大小。

空间复杂度：在序列化和反序列化函数中，我们递归会使用栈空间，故渐进空间复杂度为 O(n)。





### [<font style="background-color:rgb(240, 240, 240);">打家劫舍 III （337）</font>](https://leetcode.cn/problems/house-robber-iii/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">除了 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">两个直接相连的房子在同一天晚上被打劫</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，房屋将自动报警。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定二叉树的 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。返回 </font>_**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在不触动警报的情况下</font>**__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，小偷能够盗取的最高金额</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736765866368-142b3baa-9fad-49c2-bf16-7fc5fe8b9573.jpeg)

```plain
输入: root = [3,2,3,null,3,null,1]
输出: 7 
解释: 小偷一晚能够盗取的最高金额 3 + 3 + 1 = 7
```

```python
# 简化一下这个问题：一棵二叉树，树上的每个点都有对应的权值，每个点有两种状态（选中和不选中），问在不能同时选中有父子关系的点的情况下，能选中的点的最大权值和是多少。

# 我们可以用 f(o) 表示选择 o 节点的情况下，o 节点的子树上被选择的节点的最大权值和；g(o) 表示不选择 o 节点的情况下，o 节点的子树上被选择的节点的最大权值和；l 和 r 代表 o 的左右孩子。

# 当 o 不被选中时，o 的左右孩子可以被选中，也可以不被选中。对于 o 的某个具体的孩子 x，它对 o 的贡献是 x 被选中和不被选中情况下权值和的较大值。故 g(o)=max{f(l),g(l)}+max{f(r),g(r)}。
# 至此，我们可以用哈希表来存 f 和 g 的函数值，用深度优先搜索的办法后序遍历这棵二叉树，我们就可以得到每一个节点的 f 和 g。根节点的 f 和 g 的最大值就是我们要找的答案。

class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> (int, int):
            if node is None:  # 递归边界
                return 0, 0  # 没有节点，怎么选都是 0
            l_rob, l_not_rob = dfs(node.left)  # 递归左子树
            r_rob, r_not_rob = dfs(node.right)  # 递归右子树
            rob = l_not_rob + r_not_rob + node.val  # 选
            not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob)  # 不选
            return rob, not_rob
        return max(dfs(root))  # 根节点选或不选的最大值
```

我们可以看出，以上的算法对二叉树做了一次后序遍历，时间复杂度是 O(n)；

由于递归会使用到栈空间，空间代价是 O(n)，哈希表的空间代价也是 O(n)，故空间复杂度也是 O(n)。





### [<font style="background-color:rgb(240, 240, 240);"> 路径总和 III（437）</font>](https://leetcode.cn/problems/path-sum-iii/)（DFS）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个二叉树的根节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，和一个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">targetSum</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，求该二叉树里节点值之和等于</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">targetSum</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">路径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的数目。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">路径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736824014619-c25f998e-141b-4d9c-bc89-ef09e47b6297.jpeg)

```plain
输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：和等于 8 的路径有 3 条，如图所示。
```

```python
class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        #穷举所有的可能，我们访问每一个节点 node，检测以 node 为起始节点且向下延深的路径有多少种。我们递归遍历每一个节点的所有可能的路径，然后将这些路径数目加起来即为返回结果。
        #rootSum(p,val) 表示以节点 p 为起点向下且满足路径总和为 val 的路径数目
        #我们对二叉树上每个节点 p 求出 rootSum(p,targetSum)，然后对这些路径数目求和即为返回结果。
        def rootSum(root, targetSum):
            if root is None:
                return 0

            ret = 0
            if root.val == targetSum:
                ret += 1
            #我们对节点 p 求 rootSum(p,targetSum) 时，以当前节点 p 为目标路径的起点递归向下进行搜索。假设当前的节点 p 的值为 val，我们对左子树和右子树进行递归搜索，对节点 p 的左孩子节点 pl​求出 rootSum(pl,targetSum−val)，以及对右孩子节点 pr 求出 rootSum(pr,targetSum−val)。节点 p 的 rootSum(p,targetSum) 即等于 rootSum(pl,targetSum−val) 与 rootSum(pr,targetSum−val) 之和，同时我们还需要判断一下当前节点 p 的值是否刚好等于 targetSum。
            ret += rootSum(root.left, targetSum - root.val)
            ret += rootSum(root.right, targetSum - root.val)
            return ret
        
        if root is None:
            return 0
            
        ret = rootSum(root, targetSum)
        ret += self.pathSum(root.left, targetSum)
        ret += self.pathSum(root.right, targetSum)
        return ret
```

时间复杂度：O(N ^2)，其中 N 为该二叉树节点的个数。对于每一个节点，求以该节点为起点的路径数目时，则需要遍历以该节点为根节点的子树的所有节点，因此求该路径所花费的最大时间为 O(N)，我们会对每个节点都求一次以该节点为起点的路径数目，因此时间复杂度为 O(N^2 )。

空间复杂度：O(N)，考虑到递归需要在栈上开辟空间。







### [<font style="background-color:rgb(240, 240, 240);">把二叉搜索树转换为累加树（538）</font>](https://leetcode.cn/problems/convert-bst-to-greater-tree/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给出二叉</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">搜索</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">树的根节点，该树的节点值各不相同，请你将其转换为累加树（Greater Sum Tree），使每个节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">node</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的新值等于原树中大于或等于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">node.val</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的值之和。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">提醒一下，二叉搜索树满足下列约束条件：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点的左子树仅包含键</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">小于</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点键的节点。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点的右子树仅包含键</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">大于</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">节点键的节点。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">左右子树也必须是二叉搜索树。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">本题和 1038: </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">https://leetcode-cn.com/problems/binary-search-tree-to-greater-sum-tree/</font>](https://leetcode-cn.com/problems/binary-search-tree-to-greater-sum-tree/)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 相同</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736838059625-cf74a995-e1ae-48e1-b90b-1ab532ab3449.png)

```plain
输入：[4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
输出：[30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

```python
class Solution:
    def convertBST(self, root: TreeNode) -> TreeNode:
        #二叉搜索树是一棵空树，或者是具有下列性质的二叉树：
        # 若它的左子树不空，则左子树上所有节点的值均小于它的根节点的值；
        # 若它的右子树不空，则右子树上所有节点的值均大于它的根节点的值；
        # 它的左、右子树也分别为二叉搜索树。
        # 由这样的性质我们可以发现，二叉搜索树的中序遍历是一个单调递增的有序序列。如果我们反序地中序遍历该二叉搜索树，即可得到一个单调递减的有序序列。

        #本题中要求我们将每个节点的值修改为原来的节点值加上所有大于它的节点值之和。这样我们只需要反序中序遍历该二叉搜索树，记录过程中的节点值之和，并不断更新当前遍历到的节点的节点值，即可得到题目要求的累加树。
        def dfs(root: TreeNode):
            nonlocal total
            if root:
                dfs(root.right)
                total += root.val
                root.val = total
                dfs(root.left)
        
        total = 0
        dfs(root)
        return root
```

时间复杂度：O(n)，其中 n 是二叉搜索树的节点数。每一个节点恰好被遍历一次。

空间复杂度：O(n)，为递归过程中栈的开销，平均情况下为 O(logn)，最坏情况下树呈现链状，为 O(n)。





### [<font style="background-color:rgb(240, 240, 240);"> 二叉树的直径（543）</font>](https://leetcode.cn/problems/diameter-of-binary-tree/)<font style="background-color:rgb(240, 240, 240);">（DFS）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一棵二叉树的根节点，返回该树的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">直径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">二叉树的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">直径</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是指树中任意两个节点之间最长路径的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">长度</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。这条路径可能经过也可能不经过根节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">两节点之间路径的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">长度</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 由它们之间边数表示。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736840952282-99381638-3a09-4e1d-aff2-034b004c840c.jpeg)

```plain
输入：root = [1,2,3,4,5]
输出：3
解释：3 ，取路径 [4,2,1,3] 或 [5,2,1,3] 的长度。
```

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # 最大深度（高度）：从根节点到叶节点最长的那条路径，上的节点数。
        # 最大路径（直径）：任意两个节点最长的那条路径，上的边数。
        #DFS求当前节点深度（高度）
        def dfs(node):
            nonlocal res
            if not node:
                return 0
            #分别求左右子树高度
            l = dfs(node.left)
            r = dfs(node.right)
            
            #左右子树深度之和就是经过当前节点的当前最大直径   记录最大直径
            res = max(res, l+r)
            
            #返回高度
            return max(l, r) + 1
        
        res = -inf
        dfs(root)
        return res
```

时间复杂度：O(N)，其中 N 为二叉树的节点数，即遍历一棵二叉树的时间复杂度，每个结点只被访问一次。

空间复杂度：O(Height)，其中 Height 为二叉树的高度。由于递归函数在递归过程中需要为每一层递归函数分配栈空间，所以这里需要额外的空间且该空间取决于递归的深度，而递归的深度显然为二叉树的高度，并且每次递归调用的函数里又只用了常数个变量，所以所需空间复杂度为 O(Height) 。



### [<font style="background-color:rgb(240, 240, 240);">合并二叉树（617）</font>](https://leetcode.cn/problems/merge-two-binary-trees/)<font style="background-color:rgb(240, 240, 240);">（前序遍历）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两棵二叉树：</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">root2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">想象一下，当你将其中一棵覆盖到另一棵之上时，两棵树上的一些节点将会重叠（而另一些不会）。你需要将这两棵树合并成一棵新二叉树。合并的规则是：如果两个节点重叠，那么将这两个节点的值相加作为合并后节点的新值；否则，</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不为</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">null 的节点将直接作为新二叉树的节点。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回合并后的二叉树。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意:</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 合并过程必须从两个树的根节点开始。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![]()

```plain
输入：root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]
输出：[3,4,5,5,4,null,7]
```

```python
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        def preorder(node1, node2):
            if not node1 and not node2:
                return 
            if not node1 and node2:
                return node2
            elif node1 and not node2:
                return node1
            
            node = TreeNode(node1.val + node2.val)
            node.left = preorder(node1.left, node2.left)
            node.right = preorder(node1.right, node2.right)
            
            return node
        
        return preorder(root1, root2)
```

时间复杂度：O(min(m,n))，其中 m 和 n 分别是两个二叉树的节点个数。对两个二叉树同时进行深度优先搜索，只有当两个二叉树中的对应节点都不为空时才会对该节点进行显性合并操作，因此被访问到的节点数不会超过较小的二叉树的节点数。

空间复杂度：O(min(m,n))，其中 m 和 n 分别是两个二叉树的节点个数。空间复杂度取决于递归调用的层数，递归调用的层数不会超过较小的二叉树的最大高度，最坏情况下，二叉树的高度等于节点数。





# 5、括号
### 有效括号
[https://leetcode.cn/problems/valid-parentheses/description/](https://leetcode.cn/problems/valid-parentheses/description/)

栈 哈希表

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个只包括</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'('</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">')'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'{'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'}'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'['</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">']'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，判断字符串是否有效。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">有效字符串需满足：</font>

1. <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">左括号必须用相同类型的右括号闭合。</font>
2. <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">左括号必须以正确的顺序闭合。</font>
3. <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每个右括号都有一个对应的相同类型的左括号。</font>

```python
class Solution:
    def isValid(self, s: str) -> bool:
        res = True
        hashmap = {
            '(':')',
            '{':'}',
            '[':']'
        }
        stack = []
        for c in s:
            if c in ['(', '{', '[']:
                stack.append(c)
            if c in [')', '}', ']']:
                if len(stack) > 0:
                    tmp = stack.pop()
                    if c == hashmap[tmp]:
                        continue
                    else:
                        res = False
                        break
                else:
                    res = False
                    break
        if len(stack) != 0:
            res = False
        return res
```

时间复杂度：O(n)，其中 n 是字符串 s 的长度。

空间复杂度：O(n+∣Σ∣)，其中 Σ 表示字符集，本题中字符串只包含 6 种括号，∣Σ∣=6。栈中的字符数量为 O(n)，而哈希表使用的空间为 O(∣Σ∣)，相加即可得到总空间复杂度。





### 括号生成
递归、回溯

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">数字 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">有效的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">括号组合。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：n = 1
输出：["()"]
```



为了生成所有序列，我们可以使用递归。长度为 n 的序列就是在长度为 n−1 的序列前加一个 ‘(’ 或 ‘)’。

为了检查序列是否有效，我们遍历这个序列，并使用一个变量 balance 表示左括号的数量减去右括号的数量。如果在遍历过程中 balance 的值小于零，或者结束时 balance 的值不为零，那么该序列就是无效的，否则它是有效的。

  
方法一还有改进的余地：我们可以只在序列仍然保持有效时才添加 ‘(’ 或 ‘)’，而不是像 方法一 那样每次添加。我们可以通过跟踪到目前为止放置的左括号和右括号的数目来做到这一点，

如果左括号数量不大于 n，我们可以放一个左括号。如果右括号数量小于左括号的数量，我们可以放一个右括号

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        def traceback(tmp_list, left, right):
          if len(tmp_list) == 2*n:
            res.append("".join(tmp_list))
          
          #如果左括号数量不大于 n，我们可以放一个左括号
          if left < n:
            tmp_list.append("(")
            traceback(tmp_list, left+1, right)
            tmp_list.pop()
          #如果右括号数量小于左括号的数量，我们可以放一个右括号
          if right < left:
            tmp_list.append(")")
            traceback(tmp_list, left, right+1)
            tmp_list.pop()
      
        traceback([], 0, 0)
        return res
```

时间复杂度：O(2^2n*n)，对于 2^2n 个序列中的每一个，我们用于建立和验证该序列的复杂度为 O(n)。

空间复杂度：O(n)，除了答案数组之外，我们所需要的空间取决于递归栈的深度，每一层递归函数需要 O(1) 的空间，最多递归 2n 层，因此空间复杂度为 O(n)。







### [最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/)
栈/动态规划

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个只包含 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">'('</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">')'</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的字符串，找出最长有效（格式正确且连续）括号</font><font style="background-color:rgb(240, 240, 240);">子串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的长度。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"
```

```python
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        tag = [0 for i in range(len(s))]
        #初始化栈
        stack = []
        for i in range(len(s)):
            #左括号入栈
            if s[i] == '(':
                stack.append(i)
            #右括号出栈
            elif stack:
                j = stack.pop()
                #在配对成功的位置上标记为1
                tag[i], tag[j] = 1, 1
        
        #统计最长的连续为1的子串长度
        count = 0
        res = 0
        for label in tag:
            if label == 1:
                count += 1
                res = max(res, count)
            else:
                count = 0
        return res
```

时间复杂度： O(n)，n 是给定字符串的长度。我们只需要遍历字符串一次即可。

空间复杂度： O(n)。栈的大小在最坏情况下会达到 n，因此空间复杂度为 O(n) 。



### [<font style="background-color:rgb(240, 240, 240);">删除无效的括号（301）</font>](https://leetcode.cn/problems/remove-invalid-parentheses/)（DFS）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个由若干括号和字母组成的字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，删除最小数量的无效括号，使得输入的字符串有效。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回所有可能的结果。答案可以按 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">任意顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 返回。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：s = "()())()"
输出：["(())()","()()()"]
```

```python
class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        lens = len(s)
        
        l = r = 0
        for c in s:
            if c == '(':
                l += 1
            elif c == ')':
                if l:
                    l -= 1
                else:
                    r += 1

        res = []
        
        # idx：当前字符的索引
        # cl：保留的左括号数量
        # cr：保留的右括号数量
        # dl：需要移除的左括号数量
        # dr：需要移除的右括号数量
        # path：保留下来的字符串
        
        # cl,cr分别是统计当前的左右括号数量，我们知道右括号永远不该比左括号多。
        # dl,dr是统计当前删掉的左右括号个数，我们总共需要分别删最开始统计的l和r。
        # 然后递归就是要么删掉左括号、要么删掉右括号、要么保留当前符号

        from functools import lru_cache
        @lru_cache(maxsize=None)
        def dfs(idx, cl, cr, dl, dr, path):
            if idx == lens:
                if not dl and not dr:
                    res.append(path)
                return 

            # 若当前保留的右括号大于左括号，那必然部合法了
            # 移除的左括号，右括号超出了，那不行
            if cr>cl or dl<0 or dr<0:
                return 

            c = s[idx]

            # 移除'('，dfs下去看看行不行
            if c == '(':
                dfs(idx+1, cl, cr, dl-1, dr, path)
            # 移除')'，dfs下去看看行不行
            elif c == ')':
                dfs(idx+1, cl, cr, dl, dr-1, path)
            
            # '(', ')', 小写字母均不删除
            dfs(idx+1, cl+(c=='('), cr+(c==')'), dl, dr, path+c)


        dfs(0, 0, 0, l, r, '')

        # 如果不想最后去重，可在dfs前加记忆化搜索：@lru_cache(None)
        # return list(set(res))

        return res
```

时间复杂度：预处理 max 的复杂度为 O(n)；不考虑 score 带来的剪枝效果，最坏情况下，每个位置都有两种选择，搜索所有方案的复杂度为 O(2^n )；同时搜索过程中会产生的新字符串（最终递归树中叶子节点的字符串长度最大为 n，使用 StringBuilder 也是同理），复杂度为 O(n)。整体复杂度为 O(n∗2 ^n )

空间复杂度：最大合法方案数与字符串长度呈线性关系。复杂度为 O(n)



# 六、整数
### 10进制和2进制转换
```python
# (1) 10进制整数转2进制（字符串表达）
def decimal_to_binary_string(n):
    if n == 0:
        return '0'
    
    binary_str = ''
    while n > 0:
        remainder = n % 2
        binary_str = str(remainder) + binary_str
        n = n // 2
    return binary_str

# (2) 10进制整数转2进制（数组表达）
def decimal_to_binary_array(n):
    if n == 0:
        return [0]
    
    binary_arr = []
    while n > 0:
        remainder = n % 2
        binary_arr.insert(0, remainder)
        n = n // 2
    return binary_arr

# (3) 2进制（字符串表达）转10进制整数
def binary_string_to_decimal(binary_str):
    decimal_value = 0
    for char in binary_str:
        decimal_value = decimal_value * 2 + (ord(char) - ord('0'))
    return decimal_value

# (4) 2进制（数组表达）转10进制整数
def binary_array_to_decimal(binary_arr):
    decimal_value = 0
    for bit in binary_arr:
        decimal_value = decimal_value * 2 + bit
    return decimal_value

# 测试代码
if __name__ == "__main__":
    # 测试 (1)
    print(decimal_to_binary_string(5))  # 输出: '101'
    
    # 测试 (2)
    print(decimal_to_binary_array(5))  # 输出: [1, 0, 1]
    
    # 测试 (3)
    print(binary_string_to_decimal('101'))  # 输出: 5
    
    # 测试 (4)
    print(binary_array_to_decimal([1, 0, 1]))  # 输出: 5
```

### 整数反转
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个 32 位的有符号整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回将 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中的数字部分反转后的结果。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果反转后整数超过 32 位的有符号整数的范围 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[−2</font><sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">31</font></sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">,  2</font><sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">31 </font></sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">− 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，就返回 0。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">假设环境不允许存储 64 位整数（有符号或无符号）。</font>**

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：x = 123
输出：321
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：x = -123
输出：-321
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 3：</font>**

```plain
输入：x = 120
输出：21
```

```python
class Solution:
    def reverse(self, x: int) -> int:
        INT_MIN, INT_MAX = -2**31, 2**31 - 1
        if x == 0 : return 0
        elif x < 0 : 
            x *= -1
            flag = -1
        else:
            flag = 1
        
        value_list = []
        while x > 0:
            val = x % 10
            x = x // 10
            value_list.append(val)
        
        # if 0 in value_list : 
            # value_list.remove(0)
        for i in range(0, len(value_list)):
            if value_list[i] != 0:
                break
        value_list = value_list[i:]


        res = 0
        n = len(value_list)
        for i in range(0, n):
            res += value_list[i]*pow(10,n-i-1)

        if res > INT_MAX :
            return 0
        return res * flag
```

```python
class Solution:
    def reverse(self, x: int) -> int:
        INT_MIN, INT_MAX = -2**31, 2**31 - 1

        rev = 0
        while x != 0:
            # INT_MIN 也是一个负数，不能写成 rev < INT_MIN // 10
            if rev < INT_MIN // 10 + 1 or rev > INT_MAX // 10:
                return 0
            digit = x % 10
            # Python3 的取模运算在 x 为负数时也会返回 [0, 9) 以内的结果，因此这里需要进行特殊判断
            if x < 0 and digit > 0:
                digit -= 10

            # 同理，Python3 的整数除法在 x 为负数时会向下（更小的负数）取整，因此不能写成 x //= 10
            x = (x - digit) // 10
            rev = rev * 10 + digit
        
        return rev
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">lo</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">g</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∣</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">∣</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。翻转的次数即</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">十进制的位数。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



### 回文数
双指针

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x>= 0 and x <= 9 :
            return True
        elif x <0 :
            return False
        
        x = str(x)
        
        res = True
        left = 0
        right = len(x) - 1
        while left <= right:
            if x[left] != x[right]:
                res = False
                break
            left +=1
            right -=1
            
        return res
```

时间/空间：O(N)



### 整数转罗马数字
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">七个不同的符号代表罗马数字，其值如下：</font>

| **<font style="color:rgb(38, 38, 38);">符号</font>** | **<font style="color:rgb(38, 38, 38);">值</font>** |
| --- | --- |
| <font style="color:rgb(38, 38, 38);">I</font> | <font style="color:rgb(38, 38, 38);">1</font> |
| <font style="color:rgb(38, 38, 38);">V</font> | <font style="color:rgb(38, 38, 38);">5</font> |
| <font style="color:rgb(38, 38, 38);">X</font> | <font style="color:rgb(38, 38, 38);">10</font> |
| <font style="color:rgb(38, 38, 38);">L</font> | <font style="color:rgb(38, 38, 38);">50</font> |
| <font style="color:rgb(38, 38, 38);">C</font> | <font style="color:rgb(38, 38, 38);">100</font> |
| <font style="color:rgb(38, 38, 38);">D</font> | <font style="color:rgb(38, 38, 38);">500</font> |
| <font style="color:rgb(38, 38, 38);">M</font> | <font style="color:rgb(38, 38, 38);">1000</font> |


<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">罗马数字是通过添加从最高到最低的小数位值的转换而形成的。将小数位值转换为罗马数字有以下规则：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果该值不是以 4 或 9 开头，请选择可以从输入中减去的最大值的符号，将该符号附加到结果，减去其值，然后将其余部分转换为罗马数字。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果该值以 4 或 9 开头，使用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">减法形式</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示从以下符号中减去一个符号，例如 4 是 5 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">V</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">) 减 1 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">I</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">):</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IV</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，9 是 10 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">) 减 1 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">I</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)：</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IX</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。仅使用以下减法形式：4 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IV</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)，9 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">IX</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)，40 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">XL</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)，90 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">XC</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)，400 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">CD</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">) 和 900 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">CM</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">只有 10 的次方（</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">I</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">,</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">X</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">,</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">,</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">M</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）最多可以连续附加 3 次以代表 10 的倍数。你不能多次附加 5 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">V</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)，50 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">) 或 500 (</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">D</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">)。如果需要将符号附加4次，请使用</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">减法形式</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个整数，将其转换为罗马数字。</font>

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        hashmap = {1000:'M', 900:'CM', 500:'D', 400:'CD', 100:'C', 90:'XC', 50:'L', 40:'XL', 10:'X', 9:'IX', 5:'V', 4:'IV', 1:'I'}
        res = ''
        for key in hashmap.keys():
            tmp = num // key
            # res += "".join([hashmap[key] for i in range(tmp)])
            res += hashmap[key] * tmp
            num = num % key
        
        return res
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。最坏条件下，循环的次数为哈希表的长度。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>



### [螺旋矩阵2(59)](https://leetcode.cn/problems/spiral-matrix-ii/description/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个正整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，生成一个包含</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font><sup><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font></sup>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 所有元素，且元素按顺时针顺序螺旋排列的 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n x n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">正方形矩阵</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">matrix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1740930300735-1f35ce49-2152-4262-a345-5daa745a1306.jpeg)

```plain
输入：n = 3
输出：[[1,2,3],[8,9,4],[7,6,5]]
```

初始化一个 n×n 大小的矩阵 mat，然后模拟整个向内环绕的填入过程：

1. 定义当前左右上下边界 l,r,t,b，初始值 num = 1，迭代终止值 tar = n * n；
2. 当 num <= tar 时，始终按照 从左到右 从上到下 从右到左 从下到上 填入顺序循环，每次填入后：
    - **执行 num += 1**：得到下一个需要填入的数字；
    - **更新边界**：例如从左到右填完后，上边界 t += 1，相当于上边界向内缩 1。
3. 使用num <= tar而不是l < r || t < b作为迭代条件，是为了解决当n为奇数时，矩阵中心数字无法在迭代过程中被填充的问题。
4. 最终返回 mat 即可。

```python
class Solution:
    def generateMatrix(self, n: int) -> [[int]]:
        l, r, t, b = 0, n - 1, 0, n - 1
        mat = [[0 for _ in range(n)] for _ in range(n)]
        num, tar = 1, n * n
        while num <= tar:
            for i in range(l, r + 1): # left to right
                mat[t][i] = num
                num += 1
            t += 1
            for i in range(t, b + 1): # top to bottom
                mat[i][r] = num
                num += 1
            r -= 1
            for i in range(r, l - 1, -1): # right to left
                mat[b][i] = num
                num += 1
            b -= 1
            for i in range(b, t - 1, -1): # bottom to top
                mat[i][l] = num
                num += 1
            l += 1
        return mat

```

时间复杂度：O(n<sup>2</sup>)，其中 n 是给定的正整数。矩阵的大小是 n×n，需要填入矩阵中的每个元素。

空间复杂度：O(1)。除了返回的矩阵以外，空间复杂度是常数。

### [<font style="background-color:rgb(240, 240, 240);">爬楼梯（70）</font>](https://leetcode.cn/problems/climbing-stairs/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">假设你正在爬楼梯。需要</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 阶你才能到达楼顶。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">每次你可以爬 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 或 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个台阶。你有多少种不同的方法可以爬到楼顶呢？</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶
```

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        #dp[i]表示爬到第i个台阶的方法数量
        #dp[i] = dp[i-1] + dp[i-2]
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0 for i in range(n)]
        dp[0] = 1
        dp[1] = 2
        for i in range(2, n):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n-1]
```

  
时间复杂度：循环执行 n 次，每次花费常数的时间代价，故渐进时间复杂度为 O(n)。

空间复杂度：这里只用了常数个变量作为辅助空间，故渐进空间复杂度为 O(1)。





### [<font style="background-color:rgb(240, 240, 240);">完全平方数（279）</font>](https://leetcode.cn/problems/perfect-squares/)（DP）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和为</font>__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>__<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的完全平方数的最少数量</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">完全平方数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">4</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">、</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">9</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">16</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 都是完全平方数，而 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">3</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">11</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 不是。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：n = 12
输出：3 
解释：12 = 4 + 4 + 4
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736498966265-2e92c12f-27d0-4b64-87ed-6444bc6fbcbe.png)

```python
class Solution:
    def numSquares(self, n: int) -> int:
        #dp[i] 表示最少需要多少个数的平方来表示整数 i。
        dp = [i for i in range(n+1)]
        for i in range(1, n+1):
            for j in range(1, math.floor(math.sqrt(i))+1):
                dp[i] = min(dp[i], dp[i-j**2]+1)
        
        return dp[n]
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736498925247-860ea550-3f52-4aa0-9e87-f5a0985d6887.png)



### [<font style="background-color:rgb(240, 240, 240);">比特位计数（338）</font>](https://leetcode.cn/problems/counting-bits/)<font style="background-color:rgb(240, 240, 240);">（DP）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，对于 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0 <= i <= n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中的每个 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，计算其二进制表示中 </font>`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>**`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的个数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回一个长度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n + 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">ans</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 作为答案。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：n = 2
输出：[0,1,1]
解释：
0 --> 0
1 --> 1
2 --> 10
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736767618418-c45c9e86-7a24-4d52-b063-296eb644005e.png)

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
        def countOnes(x: int) -> int:
            ones = 0
            while x > 0:
                x &= (x - 1)
                ones += 1
            return ones
        
        bits = [countOnes(i) for i in range(n + 1)]
        return bits
```

时间复杂度：O(nlogn)。需要对从 0 到 n 的每个整数使用计算「一比特数」，对于每个整数计算「一比特数」的时间都不会超过 O(logn)。

空间复杂度：O(1)。除了返回的数组以外，空间复杂度为常数。

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
    
        def decimal_to_binary_array(n):
            if n == 0:
                return 0
            
            binary_arr = []
            while n > 0:
                remainder = n % 2
                binary_arr.insert(0, remainder)
                n = n // 2
            return sum(binary_arr)
        
        res = []
        for i in range(n+1):
            res.append(decimal_to_binary_array(i))
        
        return res
```



### [<font style="background-color:rgb(240, 240, 240);">汉明距离（461）</font>](https://leetcode.cn/problems/hamming-distance/)<font style="background-color:rgb(240, 240, 240);">（位运算）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">两个整数之间的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">汉明距离</font>](https://baike.baidu.com/item/%E6%B1%89%E6%98%8E%E8%B7%9D%E7%A6%BB)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指的是这两个数字对应二进制位不同的位置的数目。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">y</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，计算并返回它们之间的汉明距离。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：x = 1, y = 4
输出：2
解释：
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑
上面的箭头指出了对应二进制位不同的位置。
```

```python
class Solution:
    def hammingDistance(self, x: int, y: int) -> int:
        def decimal_to_binary_array(n):
            if n == 0:
                return [0]
            
            binary_arr = []
            while n > 0:
                remainder = n % 2
                binary_arr.insert(0, remainder)
                n = n // 2
            return binary_arr

        bi_x = decimal_to_binary_array(x)
        bi_y = decimal_to_binary_array(y)
        
        #较小数的二进制数组开头补0
        # if x > y :
        #     bi_y = [0]*(len(bi_x) - len(bi_y)) + bi_y
        # elif x < y:
        #     bi_x = [0]*(len(bi_y) - len(bi_x)) + bi_x
        # else:
        #     return 0

        #补0方法2：补成32位
        bi_x = [0] * (31 - len(bi_x)) + bi_x
        bi_y = [0] * (31 - len(bi_y)) + bi_y
        

        res = 0
        for i in range(len(bi_x)):
            if bi_x[i] != bi_y[i]:
                res += 1
        return res
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(n)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(n)</font><font style="background-color:rgb(240, 240, 240);">。</font>

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736837572687-6deb7f1a-5f6f-4ae1-a265-68654af138f9.png)

```python
class Solution:
    def hammingDistance(self, x, y):
        return bin(x ^ y).count('1')

```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。不同语言的实现方法不一，我们可以近似认为其时间复杂度为</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

### [水壶问题（365）](https://leetcode.cn/problems/water-and-jug-problem/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">有两个水壶，容量分别为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">x</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">y</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">升。水的供应是无限的。确定是否有可能使用这两个壶准确得到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">target</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 升。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以：</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">装满任意一个水壶</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">清空任意一个水壶</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">将水从一个水壶倒入另一个水壶，直到接水壶已满，或倒水壶已空。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>

```plain
输入: x = 3,y = 5,target = 4
输出: true
解释：
按照以下步骤操作，以达到总共 4 升水：
1. 装满 5 升的水壶(0, 5)。
2. 把 5 升的水壶倒进 3 升的水壶，留下 2 升(3, 2)。
3. 倒空 3 升的水壶(0, 2)。
4. 把 2 升水从 5 升的水壶转移到 3 升的水壶(2, 0)。
5. 再次加满 5 升的水壶(2, 5)。
6. 从 5 升的水壶向 3 升的水壶倒水直到 3 升的水壶倒满。5 升的水壶里留下了 4 升水(3, 4)。
7. 倒空 3 升的水壶。现在，5 升的水壶里正好有 4 升水(0, 4)。
参考：来自著名的 "Die Hard"
```

首先对题目进行建模。观察题目可知，在任意一个时刻，此问题的状态可以由两个数字决定：X 壶中的水量，以及 Y 壶中的水量。

在任意一个时刻，我们可以且仅可以采取以下几种操作：

把 X 壶的水灌进 Y 壶，直至灌满或倒空；

把 Y 壶的水灌进 X 壶，直至灌满或倒空；

把 X 壶灌满；

把 Y 壶灌满；

把 X 壶倒空；

把 Y 壶倒空。

因此，本题可以使用深度优先搜索来解决。搜索中的每一步以 remain_x, remain_y 作为状态，即表示 X 壶和 Y 壶中的水量。在每一步搜索时，我们会依次尝试所有的操作，递归地搜索下去。这可能会导致我们陷入无止境的递归，因此我们还需要使用一个哈希结合（HashSet）存储所有已经搜索过的 remain_x, remain_y 状态，保证每个状态至多只被搜索一次。



在实际的代码编写中，由于深度优先搜索导致的递归远远超过了 Python 的默认递归层数（可以使用 sys 库更改递归层数，但不推荐这么做），因此下面的代码使用栈来模拟递归，避免了真正使用递归而导致的问题。

```python
class Solution:
    def canMeasureWater(self, x: int, y: int, z: int) -> bool:
        stack = [(0, 0)]
        self.seen = set()
        #栈来模拟递归，避免了真正使用递归而导致的问题。
        while stack:
            remain_x, remain_y = stack.pop()
            if remain_x == z or remain_y == z or remain_x + remain_y == z:
                return True
            if (remain_x, remain_y) in self.seen:
                continue
            self.seen.add((remain_x, remain_y))
            # 把 X 壶灌满。
            stack.append((x, remain_y))
            # 把 Y 壶灌满。
            stack.append((remain_x, y))
            # 把 X 壶倒空。
            stack.append((0, remain_y))
            # 把 Y 壶倒空。
            stack.append((remain_x, 0))
            # 把 X 壶的水灌进 Y 壶，直至灌满或倒空。
            stack.append((remain_x - min(remain_x, y - remain_y), remain_y + min(remain_x, y - remain_y)))
            # 把 Y 壶的水灌进 X 壶，直至灌满或倒空。
            stack.append((remain_x + min(remain_y, x - remain_x), remain_y - min(remain_y, x - remain_x)))
        return False
```

预备知识：贝祖定理

我们认为，每次操作只会让桶里的水总量增加 x，增加 y，减少 x，或者减少 y。

你可能认为这有问题：如果往一个不满的桶里放水，或者把它排空呢？那变化量不就不是 x 或者 y 了吗？接下来我们来解释这一点：

首先要清楚，在题目所给的操作下，两个桶不可能同时有水且不满。因为观察所有题目中的操作，操作的结果都至少有一个桶是空的或者满的；

其次，对一个不满的桶加水是没有意义的。因为如果另一个桶是空的，那么这个操作的结果等价于直接从初始状态给这个桶加满水；而如果另一个桶是满的，那么这个操作的结果等价于从初始状态分别给两个桶加满；

再次，把一个不满的桶里面的水倒掉是没有意义的。因为如果另一个桶是空的，那么这个操作的结果等价于回到初始状态；而如果另一个桶是满的，那么这个操作的结果等价于从初始状态直接给另一个桶倒满。

因此，我们可以认为每次操作只会给水的总量带来 x 或者 y 的变化量。因此我们的目标可以改写成：找到一对整数 a,b，使得

ax+by=z

而只要满足 z≤x+y，且这样的 a,b 存在，那么我们的目标就是可以达成的。这是因为：

若 a≥0,b≥0，那么显然可以达成目标。

若 a<0，那么可以进行以下操作：

往 y 壶倒水；

把 y 壶的水倒入 x 壶；

如果 y 壶不为空，那么 x 壶肯定是满的，把 x 壶倒空，然后再把 y 壶的水倒入 x 壶。

重复以上操作直至某一步时 x 壶进行了 a 次倒空操作，y 壶进行了 b 次倒水操作。

若 b<0，方法同上，x 与 y 互换。

而贝祖定理告诉我们，ax+by=z 有解当且仅当 z 是 x,y 的最大公约数的倍数。**<font style="color:#74B602;">因此我们只需要找到 x,y 的最大公约数并判断 z 是否是它的倍数即可。</font>**

```python
class Solution:
    def canMeasureWater(self, x: int, y: int, z: int) -> bool:
        if x + y < z:
            return False
        if x == 0 or y == 0:
            return z == 0 or x + y == z
        return z % math.gcd(x, y) == 0

```

# 七、排序算法
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

# 八、数组结构实现
### [<font style="background-color:rgb(240, 240, 240);">LRU 缓存（146）</font>](https://leetcode.cn/problems/lru-cache/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你设计并实现一个满足 </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">LRU (最近最少使用) 缓存</font>](https://baike.baidu.com/item/LRU)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">约束的数据结构。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">实现</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">LRUCache</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">类：</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">LRUCache(int capacity)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">以</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">正整数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">作为容量 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化 LRU 缓存</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int get(int key)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果关键字</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">存在于缓存中，则返回关键字的值，否则返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void put(int key, int value)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 如果关键字 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">已经存在，则变更其数据值 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">value</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">；如果不存在，则向缓存中插入该组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key-value</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果插入操作导致关键字数量超过 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，则应该</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">逐出</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最久未使用的关键字。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">函数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">get</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">put</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 必须以 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(1)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的平均时间复杂度运行。</font>  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736407208552-81e4ad59-23ca-4dad-a138-619ca1c7f244.png)

```python
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        # 使用伪头部和伪尾部节点    
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.size = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 如果 key 存在，先通过哈希表定位，再移到头部
        node = self.cache[key]
        self.moveToHead(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key not in self.cache:
            # 如果 key 不存在，创建一个新的节点
            node = DLinkedNode(key, value)
            # 添加进哈希表
            self.cache[key] = node
            # 添加至双向链表的头部
            self.addToHead(node)
            self.size += 1
            if self.size > self.capacity:
                # 如果超出容量，删除双向链表的尾部节点
                removed = self.removeTail()
                # 删除哈希表中对应的项
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            # 如果 key 存在，先通过哈希表定位，再修改 value，并移到头部
            node = self.cache[key]
            node.value = value
            self.moveToHead(node)
    
    def addToHead(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def removeNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def moveToHead(self, node):
        self.removeNode(node)
        self.addToHead(node)

    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：对于</font><font style="background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">put</font>`<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">和</font><font style="background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">get</font>`<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">都是</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(capacity)</font><font style="background-color:rgb(240, 240, 240);">，因为哈希表和双向链表最多存储 </font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity+1</font><font style="background-color:rgb(240, 240, 240);"> 个元素。</font>



### [**<font style="background-color:rgb(240, 240, 240);">课程表（207）</font>**](https://leetcode.cn/problems/course-schedule/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你这个学期必须选修</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">numCourses</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">门课程，记为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">numCourses - 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在选修某些课程之前需要一些先修课程。 先修课程按数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prerequisites</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给出，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prerequisites[i] = [a</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">, b</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示如果要学习课程 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">a</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">则</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">必须</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">先学习课程 </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">b</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<sub><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font></sub><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如，先修课程对 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[0, 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示：想要学习课程</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，你需要先完成课程</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你判断是否可能完成所有课程的学习？如果可以，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736424480886-8a64a6ac-c861-4ab5-91c8-bd13aa7f7c28.png)

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        edges = collections.defaultdict(list)
        visited = [0] * numCourses
        result = list()
        valid = True

        for info in prerequisites:
            edges[info[1]].append(info[0])
        
        def dfs(u: int):
            nonlocal valid
            visited[u] = 1
            for v in edges[u]:
                if visited[v] == 0:
                    dfs(v)
                    if not valid:
                        return
                elif visited[v] == 1:
                    valid = False
                    return
            visited[u] = 2
            result.append(u)
        
        for i in range(numCourses):
            if valid and not visited[i]:
                dfs(i)
        
        return valid

作者：力扣官方题解
链接：https://leetcode.cn/problems/course-schedule/solutions/359392/ke-cheng-biao-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

时间复杂度: O(n+m)，其中 n 为课程数，m 为先修课程的要求数。这其实就是对图进行深度优先搜索的时间复杂度。

空间复杂度: O(n+m)。题目中是以列表形式给出的先修课程关系，为了对图进行深度优先搜索，我们需要存储成邻接表的形式，空间复杂度为 O(n+m)。在深度优先搜索的过程中，我们需要最多 O(n) 的栈空间（递归）进行深度优先搜索，因此总空间复杂度为 O(n+m)。



### [<font style="background-color:rgb(240, 240, 240);">实现 Trie (前缀树)（208）</font>](https://leetcode.cn/problems/implement-trie-prefix-tree/)
[**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">Trie</font>**](https://baike.baidu.com/item/%E5%AD%97%E5%85%B8%E6%A0%91/9825209?fr=aladdin)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（发音类似 "try"）或者说</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">前缀树</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你实现 Trie 类：</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">Trie()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化前缀树对象。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void insert(String word)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">向前缀树中插入字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">boolean search(String word)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在前缀树中，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（即，在检索之前已经插入）；否则，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">boolean startsWith(String prefix)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 如果之前已经插入的字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的前缀之一为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prefix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例：</font>**

```plain
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]
```

```python
class Trie:

    def __init__(self):
        self.word_list = []

    def insert(self, word: str) -> None:
        self.word_list.append(word)

    def search(self, word: str) -> bool:
        return word in self.word_list

    def startsWith(self, prefix: str) -> bool:
        for word in self.word_list:
            if len(word) >= len(prefix) and word[:len(prefix)] == prefix:
                return True
        return False
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736476470551-4d685eda-b3f2-4b6f-8d2e-0c4350db5d3e.png)

```python
class Trie:
    def __init__(self):
        self.children = [None] * 26
        self.isEnd = False
    
    def searchPrefix(self, prefix: str) -> "Trie":
        node = self
        for ch in prefix:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                return None
            node = node.children[ch]
        return node

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.isEnd = True

    def search(self, word: str) -> bool:
        node = self.searchPrefix(word)
        return node is not None and node.isEnd

    def startsWith(self, prefix: str) -> bool:
        return self.searchPrefix(prefix) is not None
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736476508879-ef5aa74c-72c7-43f0-9a9b-8628b3702fb7.png)



### [<font style="background-color:rgb(240, 240, 240);"> 任务调度器（621）</font>](https://leetcode.cn/problems/task-scheduler/)<font style="background-color:rgb(240, 240, 240);">（构造）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个用字符数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">tasks</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示的 CPU 需要执行的任务列表，用字母 A 到 Z 表示，以及一个冷却时间</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。每个周期或时间间隔允许完成一项任务。任务可以按任何顺序完成，但有一个限制：两个</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">相同种类</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的任务之间必须有长度为</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的冷却时间。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回完成所有任务所需要的</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 最短时间间隔</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

**<font style="background-color:rgb(240, 240, 240);">输入：</font>**<font style="background-color:rgb(240, 240, 240);">tasks = ["A","A","A","B","B","B"], n = 2</font>

**<font style="background-color:rgb(240, 240, 240);">输出：</font>**<font style="background-color:rgb(240, 240, 240);">8</font>

**<font style="background-color:rgb(240, 240, 240);">解释：</font>**

<font style="background-color:rgb(240, 240, 240);">在完成任务 A 之后，你必须等待两个间隔。对任务 B 来说也是一样。在第 3 个间隔，A 和 B 都不能完成，所以你需要待命。在第 4 个间隔，由于已经经过了 2 个间隔，你可以再次执行 A 任务。</font>

```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        #先考虑最为简单的情况：假设只有一类任务，除了最后一个任务以外，其余任务在安排后均需要增加 n 个单位的冻结时间。
        #将任务数记为 m 个，其中前 m−1 个任务均要消耗 n+1 的单位时间，最后一个任务仅消耗 1 个单位时间，即所需要的时间为 (n+1)×(m−1)+1。

        #当存在多个任务时，由于每一类任务都需要被完成，因此本质上我们最需要考虑的是将数量最大的任务安排掉，其他任务则是间插其中。
        cnts = [0] * 26
        for c in tasks:
            cnts[ord(c) - ord('A')] += 1
        #假设数量最大的任务数为 max，共有 tot 个任务数为 max 的任务种类。
        #实际上，当任务总数不超过 (n+1)×(max−1)+tot 时，我们总能将其他任务插到空闲时间中去，不会引入额外的冻结时间（下左图）；而当任务数超过该值时，我们可以在将其横向添加每个 n+1 块的后面，同时不会引入额外的冻结时间
        maxv, tot = 0, 0
        for i in range(26):
            maxv = max(maxv, cnts[i])
        for i in range(26):
            tot += 1 if maxv == cnts[i] else 0
        #综上，我们所需要的最小时间为上述两种情况中的较大值即可：max(task.length,(n+1)×(max−1)+tot)
        return max(len(tasks), (n + 1) * (maxv - 1) + tot)
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">+</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">=26</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 为任务字符集大小</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

# <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">九、栈</font>
### [<font style="background-color:rgb(240, 240, 240);">最小栈（155）</font>](https://leetcode.cn/problems/min-stack/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">设计一个支持</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">push</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pop</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">top</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">操作，并能在常数时间内检索到最小元素的栈。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">实现</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MinStack</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">类:</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MinStack()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化堆栈对象。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void push(int val)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">将元素val推入堆栈。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void pop()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">删除堆栈顶部的元素。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int top()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">获取堆栈顶部的元素。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int getMin()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 获取堆栈中的最小元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]
```

```python
class MinStack:
    def __init__(self):
        #按照上面的思路，我们只需要设计一个数据结构，使得每个元素 a 与其相应的最小值 m 时刻保持一一对应。因此我们可以使用一个辅助栈，与元素栈同步插入与删除，用于存储与每个元素对应的最小值。
        self.stack = []
        #在任意一个时刻，栈内元素的最小值就存储在辅助栈的栈顶元素中。
        self.min_stack = [inf]

    def push(self, x: int) -> None:
        self.stack.append(x)
        # 当一个元素要入栈时，我们取当前辅助栈的栈顶存储的最小值，与当前元素比较得出最小值，将这个最小值插入辅助栈中；
        self.min_stack.append(min(x, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        #当一个元素要出栈时，我们把辅助栈的栈顶元素也一并弹出；
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

时间复杂度：对于题目中的所有操作，时间复杂度均为 O(1)。因为栈的插入、删除与读取操作都是 O(1)，我们定义的每个操作最多调用栈操作两次。

空间复杂度：O(n)，其中 n 为总操作数。最坏情况下，我们会连续插入 n 个元素，此时两个栈占用的空间为 O(n)。



