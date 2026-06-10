# 回文串

<!-- source: yuque://zhongxian-iiot9/hlyypb/exzfmywxh02ve5cl -->

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

