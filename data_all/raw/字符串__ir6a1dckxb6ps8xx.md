# 字符串

<!-- source: yuque://zhongxian-iiot9/hlyypb/ir6a1dckxb6ps8xx -->

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

