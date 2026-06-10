# 数组

<!-- source: yuque://zhongxian-iiot9/hlyypb/pqp57vbwxuk6is24 -->

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



### [<font style="background-color:rgb(240, 240, 240);">寻找两个正序数组的中位数（4）</font>](https://leetcode.cn/problems/median-of-two-sorted-arrays/)（二分）
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定两个大小分别为</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的正序（从小到大）数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。请你找出并返回这两个正序数组的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中位数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">算法的时间复杂度应该为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(log (m+n))</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2
```

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

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1743561234547-ed1d3d79-4987-452f-9554-a9a67579e755.jpeg)

```plain
输入：[1,8,6,2,5,4,8,3,7]
输出：49 
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。
```

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">  
</font>

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





### [删除有序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)（26）
**<font style="color:#601BDE;">解法：双指针</font>**

:::color3
<font style="color:rgb(38, 38, 38);">给你一个 </font>**<font style="color:rgb(38, 38, 38);">非严格递增排列</font>**<font style="color:rgb(38, 38, 38);"> 的数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> ，请你</font>[**<font style="color:rgb(38, 38, 38);">原地</font>**](http://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)<font style="color:rgb(38, 38, 38);"> 删除重复出现的元素，使每个元素 </font>**<font style="color:rgb(38, 38, 38);">只出现一次</font>**<font style="color:rgb(38, 38, 38);"> ，返回删除后数组的新长度。元素的 </font>**<font style="color:rgb(38, 38, 38);">相对顺序</font>**<font style="color:rgb(38, 38, 38);"> 应该保持 </font>**<font style="color:rgb(38, 38, 38);">一致</font>**<font style="color:rgb(38, 38, 38);"> 。然后返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 中唯一元素的个数。</font>

<font style="color:rgb(38, 38, 38);">考虑</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的唯一元素的数量为</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，你需要做以下事情确保你的题解可以被通过：</font>

+ <font style="color:rgb(38, 38, 38);">更改数组</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，使</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的前</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">个元素包含唯一元素，并按照它们最初在</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">中出现的顺序排列。</font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> 的其余元素与</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">的大小不重要。</font>
+ <font style="color:rgb(38, 38, 38);">返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">k</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

:::

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [1,1,2]
输出：2, nums = [1,2,_]
解释：函数应该返回新的长度 2 ，并且原数组 nums 的前两个元素被修改为 1, 2 。不需要考虑数组中超出新长度后面的元素。
```

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

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [3,2,2,3], val = 3
输出：2, nums = [2,2,_,_]
解释：你的函数函数应该返回 k = 2, 并且 nums 中的前两个元素均为 2。
你在返回的 k 个元素之外留下了什么并不重要（因此它们并不计入评测）。
```

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





### [搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)（33）（二分）
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



### [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)（34）（二分）
**<font style="color:#601BDE;">解法：两次二分法</font>**

:::color3
<font style="color:rgb(38, 38, 38);">给你一个按照非递减顺序排列的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);">，和一个目标值 </font>`<font style="color:rgba(38, 38, 38, 0.75);">target</font>`<font style="color:rgb(38, 38, 38);">。请你找出给定目标值在数组中的开始位置和结束位置。</font>

<font style="color:rgb(38, 38, 38);">如果数组中不存在目标值</font><font style="color:rgb(38, 38, 38);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);">target</font>`<font style="color:rgb(38, 38, 38);">，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">[-1, -1]</font>`<font style="color:rgb(38, 38, 38);">。</font>

<font style="color:rgb(38, 38, 38);">你必须设计并实现时间复杂度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);">O(log n)</font>`<font style="color:rgb(38, 38, 38);"> 的算法解决此问题。</font>

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



### [接雨水](https://leetcode.cn/problems/trapping-rain-water/)（42）
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



### [<font style="background-color:rgb(240, 240, 240);">跳跃游戏</font>](https://leetcode.cn/problems/jump-game/)<font style="background-color:rgb(240, 240, 240);">（55）</font>
贪心

<font style="color:rgb(38, 38, 38);">给你一个非负整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);">nums</font>`<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">，你最初位于数组的</font><font style="color:rgb(38, 38, 38);"> </font>**<font style="color:rgb(38, 38, 38);">第一个下标</font>**<font style="color:rgb(38, 38, 38);"> </font><font style="color:rgb(38, 38, 38);">。数组中的每个元素代表你在该位置可以跳跃的最大长度。</font>

<font style="color:rgb(38, 38, 38);">判断你是否能够到达最后一个下标，如果可以，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">true</font>`<font style="color:rgb(38, 38, 38);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);">false</font>`<font style="color:rgb(38, 38, 38);"> 。</font>

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

### [<font style="background-color:rgb(240, 240, 240);">合并两个有序数组（88）</font>](https://leetcode.cn/problems/merge-sorted-array/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个按</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非递减顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">排列的整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，另有两个整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，分别表示</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中的元素数目。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">合并</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums2</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">到</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">中，使合并后的数组同样按</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非递减顺序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">排列。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最终，合并后数组不应由函数返回，而是存储在数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 中。为了应对这种情况，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的初始长度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m + n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中前 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">m</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个元素表示应合并的元素，后 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 个元素为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，应忽略。</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums2</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的长度为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
输出：[1,2,2,3,5,6]
解释：需要合并 [1,2,3] 和 [2,5,6] 。
合并结果是 [1,2,2,3,5,6] ，其中斜体加粗标注的为 nums1 中的元素。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums1 = [1], m = 1, nums2 = [], n = 0
输出：[1]
解释：需要合并 [1] 和 [] 。
合并结果是 [1] 。
```

```python
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # 初始化三个指针 p1=m−1 指向 nums1的末尾，p2=n−1 指向 nums2的末尾，p=m+n−1 指向合并后的数组末尾。
        p1, p2, p = m - 1, n - 1, m + n - 1
        while p2 >= 0:  # nums2 还有要合并的元素
            # 不断比较nums1[p1]和nums2[p2]的大小，把较大的值放入nums1[p]

            # 如果 p1 >= 0，nums1[p1]更大，则把nums1[p1]放入nums1[p]
            if p1 >= 0 and nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]  # 填入 nums1[p1]
                p1 -= 1
            # 如果 p1 < 0，那么走 else 分支，把 nums2 合并到 nums1 中
            else:
                nums1[p] = nums2[p2]  # 填入 nums2[p1]
                p2 -= 1
            p -= 1  # 下一个要填入的位置


```

时间复杂度：O(m+n)。最坏情况形如 nums 1 =[4,5,6,∗,∗,∗],nums 2 =[1,2,3]，每个数都需要移动一次。

空间复杂度：O(1)。仅用到若干额外变量。



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



### 数组中的前 K 个最大元素
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定整数数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">nums</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和整数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请返回数组中</font><font style="color:#DF2A3F;background-color:rgb(240, 240, 240);">前 </font>`**<font style="color:#DF2A3F;background-color:rgb(240, 240, 240);">k</font>**`<font style="color:#DF2A3F;background-color:rgb(240, 240, 240);"> 个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最大的元素。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请注意，你需要找的是数组排序后的</font><font style="color:#DF2A3F;background-color:rgb(240, 240, 240);">前 </font>`<font style="color:#DF2A3F;background-color:rgb(240, 240, 240);">k</font>`<font style="color:#DF2A3F;background-color:rgb(240, 240, 240);"> 个</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最大的元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [3,2,1,5,6,4], k = 2
输出：[6,5]
```

```python
import random

def partition(nums, left, right):
    # 随机选择枢轴，并将其放到最右侧
    pivot_index = random.randint(left, right)
    nums[pivot_index], nums[right] = nums[right], nums[pivot_index]
    pivot = nums[right]
    
    # 分区操作
    i = left
    for j in range(left, right):
        if nums[j] > pivot:  # 按降序排列
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    
    # 将枢轴放回正确位置
    nums[i], nums[right] = nums[right], nums[i]
    return i

def quick_select(nums, left, right, k):
    if left <= right:
        # 获取分区点
        pivot_index = partition(nums, left, right)
        
        # 如果分区点正好是第 k 个元素
        if pivot_index == k - 1:
            return nums[:k]
        # 如果分区点在目标位置左侧，继续处理右侧
        elif pivot_index < k - 1:
            return quick_select(nums, pivot_index + 1, right, k)
        # 如果分区点在目标位置右侧，继续处理左侧
        else:
            return quick_select(nums, left, pivot_index - 1, k)

def top_k_largest(nums, k):
    # 调用快速选择算法
    return quick_select(nums, 0, len(nums) - 1, k)

# 示例输入
nums = [1, 2, 4, 3]
k = 2
result = top_k_largest(nums, k)
print(result)  # 输出 [3, 4]
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

### [<font style="background-color:rgb(240, 240, 240);">打家劫舍 II（213）</font>](https://leetcode.cn/problems/house-robber-ii/)
<font style="color:rgb(38, 38, 38);">你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都 </font>**<font style="color:rgb(38, 38, 38);">围成一圈</font>**<font style="color:rgb(38, 38, 38);"> ，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，</font>**<font style="color:rgb(38, 38, 38);">如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警</font>**<font style="color:rgb(38, 38, 38);"> 。</font>

<font style="color:rgb(38, 38, 38);">给定一个代表每个房屋存放金额的非负整数数组，计算你 </font>**<font style="color:rgb(38, 38, 38);">在不触动警报装置的情况下</font>**<font style="color:rgb(38, 38, 38);"> ，今晚能够偷窃到的最高金额。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：nums = [2,3,2]
输出：3
解释：你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：nums = [1,2,3,1]
输出：4
解释：你可以先偷窃 1 号房屋（金额 = 1），然后偷窃 3 号房屋（金额 = 3）。
     偷窃到的最高金额 = 1 + 3 = 4 。
```

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        # 假设偷窃房屋的下标范围是 [start,end]，用 dp[i] 表示在下标范围 [start,i] 内可以偷窃到的最高总金额，那么就有如下的状态转移方程：
        # dp[i]=max(dp[i−2]+nums[i],dp[i−1])

        # 边界条件为：
        # dp[start]=nums[start]  只有一间房屋，则偷窃该房屋
        # dp[start+1]=max(nums[start],nums[start+1])  只有两间房屋，偷窃其中金额较高的房屋

        # 计算得到 dp[end] 即为下标范围 [start,end] 内可以偷窃到的最高总金额。
        def robRange(start: int, end: int) -> int:
            first = nums[start]
            second = max(nums[start], nums[start + 1])
            for i in range(start + 2, end + 1):
                first, second = second, max(first + nums[i], second)
            return second
        
        length = len(nums)
        if length == 1:
            return nums[0]
        elif length == 2:
            return max(nums[0], nums[1])
        else:
            return max(robRange(0, length - 2), robRange(1, length - 1))

```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是数组长度。需要对数组遍历两次，计算可以偷窃到的最高总金额。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



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

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
```

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

