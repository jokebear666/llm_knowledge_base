# 子数组和

<!-- source: yuque://zhongxian-iiot9/hlyypb/pxn9mewqiexamfsl -->

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



