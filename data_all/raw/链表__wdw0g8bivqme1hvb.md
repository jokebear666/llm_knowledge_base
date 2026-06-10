# 链表

<!-- source: yuque://zhongxian-iiot9/hlyypb/wdw0g8bivqme1hvb -->

### 链表遍历
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def traverse_linked_list(head):
    current = head
    while current is not None:
        print(current.val)  # 打印当前节点的值
        current = current.next  # 移动到下一个节点

# 示例用法
if __name__ == "__main__":
    # 创建链表：1 -> 2 -> 3
    node1 = ListNode(1)
    node2 = ListNode(2)
    node3 = ListNode(3)
    
    node1.next = node2
    node2.next = node3
    
    # 遍历链表
    traverse_linked_list(node1)
```



### 两数相加
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">非空</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的链表，表示两个非负的整数。它们每位数字都是按照 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">逆序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的方式存储的，并且每个节点只能存储 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">一位</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 数字。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你将两个数相加，并以相同形式返回一个表示和的链表。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你可以假设除了数字 0 之外，这两个数都不会以 0 开头。</font>

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1734611593209-8f409084-3601-4c1b-9959-91803e90c5a1.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        prenode = ListNode(0)
        lastnode = prenode
        val = 0
        while val or l1 or l2:
            val, cur = divmod(val + (l1.val if l1 else 0) + (l2.val if l2 else 0), 10)
            lastnode.next = ListNode(cur)
            lastnode = lastnode.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return prenode.next
```

### 删除链表倒数第N个节点
遍历/双指针

[https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表，删除链表的倒数第 </font>`<font style="color:rgba(38, 38, 38, 0.75);">n</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个结点，并且返回链表的头结点。</font>

```plain
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        def get_length(head):
          len = 0
          while head:
            len += 1
            head = head.next
          return len
          
        dummy = ListNode(0, head)
        len = get_length(head)
        cur = dummy
        #为了与题目中的 n 保持一致，节点的编号从 1 开始，头节点为编号 1 的节点。
        for i in range(1, len-n+1):
          cur = cur.next #遍历
        cur.next = cur.next.next #修改指针
        
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的长度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        left = dummy
        right = head
        #右指针先走N步
        for i in range(0, n):
            right = right.next

        #左右指针一起走，直到右指针走完
        while right:
            right = right.next
            left = left.next
        
        left.next = left.next.next
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">L</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的长度。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>



### 合并两个有序链表
迭代/递归

[https://leetcode.cn/problems/merge-two-sorted-lists/description/](https://leetcode.cn/problems/merge-two-sorted-lists/description/)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">将两个升序链表合并为一个新的</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">升序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 </font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735539752920-bc75a9ca-bc13-4530-8cc4-2892a2ce2cdd.jpeg)

```plain
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：l1 = [], l2 = []
输出：[]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        pre = ListNode(0)
        last = pre
        
        while list1 and list2:
          if list1.val < list2.val:
            last.next = ListNode(list1.val)
            list1 = list1.next
          else:
            last.next = ListNode(list2.val)
            list2 = list2.next
          last = last.next
        
        if list1:
          last.next = list1
        if list2:
          last.next = list2
          
        return pre.next
```

时间复杂度：O(n+m)，其中 n 和 m 分别为两个链表的长度。因为每次循环迭代中，l1 和 l2 只有一个元素会被放进合并链表中， 因此 while 循环的次数不会超过两个链表的长度之和。所有其他操作的时间复杂度都是常数级别的，因此总的时间复杂度为 O(n+m)。

空间复杂度：O(1)。我们只需要常数的空间存放若干变量。



### 合并K个升序链表
[https://leetcode.cn/problems/merge-k-sorted-lists/description/](https://leetcode.cn/problems/merge-k-sorted-lists/description/)

顺序合并/分治

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表数组，每个链表都已经按升序排列。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你将所有链表合并到一个升序链表中，返回合并后的链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：lists = []
输出：[]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
                pre = ListNode(0)
                last = pre
                
                while list1 and list2:
                    if list1.val < list2.val:
                        last.next = ListNode(list1.val)
                        list1 = list1.next
                    else:
                        last.next = ListNode(list2.val)
                        list2 = list2.next
                    last = last.next
                
                if list1:
                    last.next = list1
                if list2:
                    last.next = list2
                
                return pre.next
            
            pre = ListNode(-inf)
            for i in range(0, len(lists)):
                pre = mergeTwoLists(pre, lists[i])
            
            return pre.next
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735563502665-5ac3cd72-2dd4-4a2a-8fa9-028142073fa5.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564038789-78411734-6fac-45dc-9ab4-4c3b733b4d3e.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
            def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
                pre = ListNode(0)
                last = pre
                
                while list1 and list2:
                    if list1.val < list2.val:
                        last.next = ListNode(list1.val)
                        list1 = list1.next
                    else:
                        last.next = ListNode(list2.val)
                        list2 = list2.next
                    last = last.next
                
                if list1:
                    last.next = list1
                if list2:
                    last.next = list2
                
                return pre.next
            
            #递归实现分治
            def merge(lists, l, r):
                if l == r : return lists[l]
                if l > r : return None
                mid = (l + r) // 2
                return mergeTwoLists(merge(lists, l, mid), merge(lists, mid+1, r))
            
            return merge(lists, 0, len(lists)-1)
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564021238-2891c512-2052-4a36-ab8a-a49fc8a89284.png)



### 两两交换链表中的节点
[https://leetcode.cn/problems/swap-nodes-in-pairs/description/](https://leetcode.cn/problems/swap-nodes-in-pairs/description/)

<font style="background-color:rgb(240, 240, 240);">迭代/递归</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即，只能进行节点交换）。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735564809704-6ff2befb-3fb7-4be2-804b-35f783dbe4e3.jpeg)

```plain
输入：head = [1,2,3,4]
输出：[2,1,4,3]
```

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 2：</font>**

```plain
输入：head = []
输出：[]
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564702800-b52a7e12-6fdc-4133-8787-a10a1062084a.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735564719963-af49ae7c-35ff-4e79-a121-3c79dec2158b.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head
        tmp = dummy
        
        while tmp.next and tmp.next.next:
            node1 = tmp.next
            node2 = tmp.next.next

            # 图1 交换两个节点
            tmp.next = node2
            node1.next = node2.next
            node2.next = node1

            # 图2向前移动两步（此时node1已经交换完毕）
            tmp = node1
        return dummy.next
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">是链表的节点数量。需要对每个节点进行更新指针的操作。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

<font style="background-color:rgb(240, 240, 240);"></font>

### 反转链表
[https://leetcode.cn/problems/reverse-linked-list/description/](https://leetcode.cn/problems/reverse-linked-list/description/)

迭代（双指针）/递归

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你反转链表，并返回反转后的链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735565333487-67798235-83d4-4a74-94b2-e26cb074c84a.jpeg)

```plain
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre = None
        cur = head
        while cur:
            #暂存后继节点
            tmp = cur.next
            #修改当前节点指针
            cur.next = pre
            #双指针向前移动
            pre = cur
            cur = tmp
        return pre
```

+ **<font style="background-color:rgb(240, 240, 240);">时间复杂度</font>****<font style="background-color:rgb(240, 240, 240);"> </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">N</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>****<font style="background-color:rgb(240, 240, 240);"> </font>****<font style="background-color:rgb(240, 240, 240);">：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">遍历链表使用线性大小时间。</font>
+ **<font style="background-color:rgb(240, 240, 240);">空间复杂度 </font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>**_**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font>****<font style="background-color:rgb(240, 240, 240);"> ：</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 变量 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pre</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">cur</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 使用常数大小额外空间</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"></font>

### [<font style="background-color:rgb(240, 240, 240);">K 个一组翻转链表</font>](https://leetcode.cn/problems/reverse-nodes-in-k-group/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你链表的头节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，每 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">个节点一组进行翻转，请你返回修改后的链表。</font>

`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">k</font>`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的整数倍，那么请将最后剩余的节点保持原有顺序。你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2024/jpeg/29769680/1735566315916-95e64509-b54f-423c-82f5-6729b1f9fbba.jpeg)

```plain
输入：head = [1,2,3,4,5], k = 2
输出：[2,1,4,3,5]
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566153716-13813087-2db6-4c0a-be08-bbb21ddd92b3.png)

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566263872-b13f068d-6761-42b6-8f19-6c139a47fb0b.png)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
            def reverseList(head, tail):
                pre = tail.next
                cur = head
                while pre != tail:
                    #暂存后继节点
                    tmp = cur.next
                    #修改当前节点指针
                    cur.next = pre
                    #双指针向前移动
                    pre = cur
                    cur = tmp
                return tail, head
            
            dummy = ListNode(0)
            dummy.next = head
            pre = dummy

            while head:
                tail = pre

                #step1 图1 tail指针先走K步，如果走不到k步则说明已经反转完成
                for i in range(k):
                    tail = tail.next
                    if not tail:
                        return dummy.next
                
                #step2 图1 记录nex节点位置
                nex = tail.next

                #step3 图1 反转k个节点
                head, tail = reverseList(head, tail)

                #step4 图2 把子链表接回原链表
                pre.next = head
                tail.next = nex

                #step5 图2 移动pre head指针
                pre = tail
                head = tail.next
            
            return dummy.next
```

![](https://cdn.nlark.com/yuque/0/2024/png/29769680/1735566382698-9390a2cc-e3c5-4b53-ba07-85f3f900e157.png)



### [<font style="background-color:rgb(240, 240, 240);">环形链表（141）</font>](https://leetcode.cn/problems/linked-list-cycle/)
双指针  哈希表

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个链表的头节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，判断链表中是否有环。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中有某个节点，可以通过连续跟踪</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">next</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">来表示链表尾连接到链表中的位置（索引从 0 开始）。</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>**`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不作为参数进行传递 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。仅仅是为了标识链表的实际情况。</font>

_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中存在环</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，则返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。 否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736404645268-bfbdc8d2-16dc-4363-aea9-5a6ae7c8c648.png)

```plain
输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        #快慢指针
        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            #如果相遇  说明有环
            if slow == fast:
                return True
        
        return False
```

时间复杂度：O(N)，其中 N 是链表中的节点数。

当链表中不存在环时，快指针将先于慢指针到达链表尾部，链表中每个节点至多被访问两次。

当链表中存在环时，每一轮移动后，快慢指针的距离将减小一。初始距离为环的长度，因此至多移动 N 轮。

空间复杂度：O(1)。我们只使用了两个指针的额外空间。







### [<font style="background-color:rgb(240, 240, 240);">环形链表 II（142）</font>](https://leetcode.cn/problems/linked-list-cycle-ii/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给定一个链表的头节点  </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回链表开始入环的第一个节点。 </font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表无环，则返回 </font>_`_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">null</font>_`_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>_

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果链表中有某个节点，可以通过连续跟踪</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">next</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">来表示链表尾连接到链表中的位置（</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">索引从 0 开始</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">）。如果</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，则在该链表中没有环。</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意：</font>**`**<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">pos</font>**`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不作为参数进行传递</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，仅仅是为了标识链表的实际情况。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">不允许修改 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">链表。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点
解释：链表中有一个环，其尾部连接到第二个节点。
```

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        flag = 0
        while slow and fast and fast.next:
            if not (fast and fast.next): return
            slow = slow.next
            fast = fast.next.next
            #快慢指针相遇
            if slow == fast :
                #有环标记
                flag = 1 
                break

        if flag == 0:
            return None
        
        ptr = head
        while ptr != slow:
            #有了 a=c+(n−1)(b+c) 的等量关系，我们会发现：从相遇点到入环点的距离加上 n−1 圈的环长，恰好等于从链表头部到入环点的距离。
            # 因此，当发现 slow 与 fast 相遇时，我们再额外使用一个指针 ptr。起始，它指向链表头部；随后，它和 slow 每次向后移动一个位置。最终，它们会在入环点相遇。
            #第3指针和慢指针相遇点，就是入环点
            ptr = ptr.next
            slow = slow.next
        return ptr
```

时间复杂度 O(N) ：第二次相遇中，慢指针须走步数 a<a+b；第一次相遇中，慢指针须走步数 a+b−x<a+b，其中 x 为双指针重合点与环入口距离；因此总体为线性复杂度；

空间复杂度 O(1) ：双指针使用常数大小的额外空间。

```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        hashmap = set()
        
        cur = head
        while cur:
            if cur in hashmap:
                return cur
            hashmap.add(cur)
            cur = cur.next
        
        return None
```

时间复杂度：O(N)，其中 N 为链表中节点的数目。我们恰好需要访问链表中的每一个节点。

空间复杂度：O(N)，其中 N 为链表中节点的数目。我们需要将链表中的每个节点都保存在哈希表当中。





### [<font style="background-color:rgb(240, 240, 240);">排序链表（148）</font>](https://leetcode.cn/problems/sort-list/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你链表的头结点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请将其按 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">升序</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 排列并返回 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">排序后的链表</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736407916227-6d72d866-c30c-48d5-8515-0e652ab8e885.jpeg)

```plain
输入：head = [4,2,1,3]
输出：[1,2,3,4]
```



方法一：归并排序（分治）

找到链表的中间结点 head 2的前一个节点，并断开 head 2与其前一个节点的连接。这样我们就把原链表均分成了两段更短的链表。原理见【基础算法精讲 07】。

分治，递归调用 sortList，分别排序 head（只有前一半）和 head 2 。

排序后，我们得到了两个有序链表，那么合并两个有序链表，得到排序后的链表，返回链表头节点。原理见 我的题解。

```python
class Solution:
    # 876. 链表的中间结点（快慢指针）
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        # 先找到链表的中间结点的【前一个节点】
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next  # 下一个节点就是链表的中间结点 mid
        slow.next = None  # 断开 mid 的前一个节点和 mid 的连接
        return mid

    # 21. 合并两个有序链表（双指针）
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dummy = ListNode()  # 用哨兵节点简化代码逻辑
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1  # 把 list1 加到新链表中
                list1 = list1.next
            else:  # 注：相等的情况加哪个节点都是可以的
                cur.next = list2  # 把 list2 加到新链表中
                list2 = list2.next
            cur = cur.next
        cur.next = list1 if list1 else list2  # 拼接剩余链表
        return dummy.next

    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 如果链表为空或者只有一个节点，无需排序
        if head is None or head.next is None:
            return head
        # 找到中间节点，并断开 head2 与其前一个节点的连接
        # 比如 head=[4,2,1,3]，那么 middleNode 调用结束后 head=[4,2] head2=[1,3]
        head2 = self.middleNode(head)
        # 分治
        head = self.sortList(head)
        head2 = self.sortList(head2)
        # 合并
        return self.mergeTwoLists(head, head2)
```

时间复杂度：O(nlogn)，其中 n 是链表长度。递归式 T(n)=2T(n/2)+O(n)，由主定理可得时间复杂度为 O(nlogn)。

空间复杂度：O(logn)。递归需要 O(logn) 的栈开销。





### [相交链表（160）](https://leetcode.cn/problems/intersection-of-two-linked-lists/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你两个单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">headA</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">和</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">headB</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">null</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">图示两个链表在节点</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">c1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">开始相交</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">：</font>**

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736413742352-0baf7dc6-4c02-4ccb-b1c9-dec0edeeb702.png)

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">题目数据</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保证</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">整个链式结构中不存在环。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">注意</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，函数返回结果后，链表必须 </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">保持其原始结构</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
            
        #哈希表
        node_set = set()
        ptr_a, ptr_b = headA, headB
        #先遍历a
        while ptr_a:
            node_set.add(ptr_a)
            ptr_a = ptr_a.next
        #再遍历b
        while ptr_b:
            if ptr_b in node_set:
                return ptr_b
            ptr_b = ptr_b.next
        
        return None
```

时间复杂度：O(m+n)，其中 m 和 n 是分别是链表 headA 和 headB 的长度。需要遍历两个链表各一次。

空间复杂度：O(m)，其中 m 是链表 headA 的长度。需要使用哈希集合存储链表 headA 中的全部节点。

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
            
        node_set = set()
        ptr_a, ptr_b = headA, headB
        #当指针 pA 和 pB 指向同一个节点或者都为空时，返回它们指向的节点或者 null
        while ptr_a != ptr_b:
            #如果指针 pA 不为空，则将指针 pA 移到下一个节点  如果指针 pA 为空，则将指针 pA 移到链表 headB 的头节点
            ptr_a = ptr_a.next if ptr_a != None else headB
            #pB操作相同
            ptr_b = ptr_b.next if ptr_b != None else headA
        return ptr_a
            
```

时间复杂度：O(m+n)，其中 m 和 n 是分别是链表 headA 和 headB 的长度。两个指针同时遍历两个链表，每个指针遍历两个链表各一次。

空间复杂度：O(1)。



### [<font style="background-color:rgb(240, 240, 240);"> 回文链表（234）</font>](https://leetcode.cn/problems/palindrome-linked-list/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个单链表的头节点 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">head</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，请你判断该链表是否为</font><font style="background-color:rgb(240, 240, 240);">回文链表</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果是，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

![](https://cdn.nlark.com/yuque/0/2025/jpeg/29769680/1736491482814-b1f516d7-c19a-4d7f-bbc1-023d2a76191a.jpeg)

```plain
输入：head = [1,2,2,1]
输出：true
```

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        def reverse_list(node):
            pre = None
            cur = node
            while cur:
                #暂存后继节点
                tmp = cur.next
                #修改当前节点指针
                cur.next = pre
                #双指针向前移动
                pre = cur
                cur = tmp
            return pre

        def find_middle_node(node):
            slow, fast = node, node
            while fast and fast.next:
                slow = slow.next
                fast = fast.next.next
            return slow
        
        if not head:
            return False

        
        #找到中间节点
        first_half_end = find_middle_node(head)
        
        #反转链表后一半
        second_half_start = reverse_list(first_half_end)
        
        #判断前一半和后一半的反转是否一致
        n1, n2 = head, second_half_start
        while n1 and n2:
            if n1.val != n2.val:
                return False
            n1 = n1.next
            n2 = n2.next
        
        #恢复链表后一半    
        first_half_end.next = reverse_list(second_half_start)
        
        return True
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">，其中</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">指的是链表的大小。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。我们只会修改原本链表中节点的指向，而在堆栈上的堆栈帧不超过 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(1)</font><font style="background-color:rgb(240, 240, 240);">。</font>

```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        def reverse_list(node):
            pre = None
            cur = node
            while cur:
                #暂存后继节点
                tmp = cur.next
                #修改当前节点指针
                cur.next = pre
                #双指针向前移动
                pre = cur
                cur = tmp
            return pre

        
        head2 = reverse_list(copy.deepcopy(head))
        
        n1, n2 = head, head2
        while n1 and n2:
            if n1.val != n2.val:
                return False
            n1 = n1.next
            n2 = n2.next
        return True
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">指的是链表的大小。</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 指的是链表的大小。</font>

