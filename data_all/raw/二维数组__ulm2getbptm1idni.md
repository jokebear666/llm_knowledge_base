# 二维数组

<!-- source: yuque://zhongxian-iiot9/hlyypb/ulm2getbptm1idni -->

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



