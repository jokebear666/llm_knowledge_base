# 子数组/子序列/子集

<!-- source: yuque://zhongxian-iiot9/hlyypb/bxh0m0z90ai8a2gi -->

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



