# 二叉树

<!-- source: yuque://zhongxian-iiot9/hlyypb/qlzs7ch1pmse8vfu -->

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



- [ ] [**<font style="background-color:rgb(240, 240, 240);">101. 对称二叉树</font>**](https://leetcode.cn/problems/symmetric-tree/)

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



