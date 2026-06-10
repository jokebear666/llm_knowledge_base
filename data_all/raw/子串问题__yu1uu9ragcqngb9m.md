# 子串问题

<!-- source: yuque://zhongxian-iiot9/hlyypb/yu1uu9ragcqngb9m -->

### 最长不重复子串
滑动窗+双指针

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);">s</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你找出其中不含有重复字符的 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最长 </font>****<font style="background-color:rgb(240, 240, 240);">子串</font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的长度。</font>

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

