# 栈

<!-- source: yuque://zhongxian-iiot9/hlyypb/sxkgm6nembgrakg9 -->



### [<font style="background-color:rgb(240, 240, 240);">最小栈（155）</font>](https://leetcode.cn/problems/min-stack/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">设计一个支持</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">push</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pop</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，</font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">top</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">操作，并能在常数时间内检索到最小元素的栈。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">实现</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MinStack</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">类:</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">MinStack()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化堆栈对象。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void push(int val)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">将元素val推入堆栈。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void pop()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">删除堆栈顶部的元素。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int top()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">获取堆栈顶部的元素。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int getMin()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 获取堆栈中的最小元素。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1:</font>**

```plain
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]
```

```python
class MinStack:
    def __init__(self):
        #按照上面的思路，我们只需要设计一个数据结构，使得每个元素 a 与其相应的最小值 m 时刻保持一一对应。因此我们可以使用一个辅助栈，与元素栈同步插入与删除，用于存储与每个元素对应的最小值。
        self.stack = []
        #在任意一个时刻，栈内元素的最小值就存储在辅助栈的栈顶元素中。
        self.min_stack = [inf]

    def push(self, x: int) -> None:
        self.stack.append(x)
        # 当一个元素要入栈时，我们取当前辅助栈的栈顶存储的最小值，与当前元素比较得出最小值，将这个最小值插入辅助栈中；
        self.min_stack.append(min(x, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        #当一个元素要出栈时，我们把辅助栈的栈顶元素也一并弹出；
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

时间复杂度：对于题目中的所有操作，时间复杂度均为 O(1)。因为栈的插入、删除与读取操作都是 O(1)，我们定义的每个操作最多调用栈操作两次。

空间复杂度：O(n)，其中 n 为总操作数。最坏情况下，我们会连续插入 n 个元素，此时两个栈占用的空间为 O(n)。



