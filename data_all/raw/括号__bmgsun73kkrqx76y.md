# 括号

<!-- source: yuque://zhongxian-iiot9/hlyypb/bmgsun73kkrqx76y -->

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

