# 排列

<!-- source: yuque://zhongxian-iiot9/hlyypb/dqtkcwwhiff99ebg -->

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

