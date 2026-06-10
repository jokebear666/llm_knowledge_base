# 数据结构实现

<!-- source: yuque://zhongxian-iiot9/hlyypb/vbqpq4zdgfbz9os1 -->

### [<font style="background-color:rgb(240, 240, 240);">LRU 缓存（146）</font>](https://leetcode.cn/problems/lru-cache/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你设计并实现一个满足 </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>[<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">LRU (最近最少使用) 缓存</font>](https://baike.baidu.com/item/LRU)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">约束的数据结构。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">实现</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">LRUCache</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">类：</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">LRUCache(int capacity)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">以</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">正整数</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">作为容量 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化 LRU 缓存</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">int get(int key)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果关键字</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">存在于缓存中，则返回关键字的值，否则返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">-1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void put(int key, int value)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 如果关键字 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">已经存在，则变更其数据值 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">value</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">；如果不存在，则向缓存中插入该组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">key-value</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。如果插入操作导致关键字数量超过 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，则应该</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">逐出</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">最久未使用的关键字。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">函数 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">get</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 和 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">put</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 必须以 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O(1)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的平均时间复杂度运行。</font>  
![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736407208552-81e4ad59-23ca-4dad-a138-619ca1c7f244.png)

```python
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = dict()
        # 使用伪头部和伪尾部节点    
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.size = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 如果 key 存在，先通过哈希表定位，再移到头部
        node = self.cache[key]
        self.moveToHead(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key not in self.cache:
            # 如果 key 不存在，创建一个新的节点
            node = DLinkedNode(key, value)
            # 添加进哈希表
            self.cache[key] = node
            # 添加至双向链表的头部
            self.addToHead(node)
            self.size += 1
            if self.size > self.capacity:
                # 如果超出容量，删除双向链表的尾部节点
                removed = self.removeTail()
                # 删除哈希表中对应的项
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            # 如果 key 存在，先通过哈希表定位，再修改 value，并移到头部
            node = self.cache[key]
            node.value = value
            self.moveToHead(node)
    
    def addToHead(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def removeNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def moveToHead(self, node):
        self.removeNode(node)
        self.addToHead(node)

    def removeTail(self):
        node = self.tail.prev
        self.removeNode(node)
        return node
```

+ <font style="background-color:rgb(240, 240, 240);">时间复杂度：对于</font><font style="background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">put</font>`<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">和</font><font style="background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">get</font>`<font style="background-color:rgb(240, 240, 240);"> </font><font style="background-color:rgb(240, 240, 240);">都是</font><font style="background-color:rgb(240, 240, 240);"> </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="background-color:rgb(240, 240, 240);">。</font>
+ <font style="background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(capacity)</font><font style="background-color:rgb(240, 240, 240);">，因为哈希表和双向链表最多存储 </font><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">capacity+1</font><font style="background-color:rgb(240, 240, 240);"> 个元素。</font>



### [**<font style="background-color:rgb(240, 240, 240);">课程表（207）</font>**](https://leetcode.cn/problems/course-schedule/)
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">你这个学期必须选修</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">numCourses</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">门课程，记为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 到 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">numCourses - 1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在选修某些课程之前需要一些先修课程。 先修课程按数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prerequisites</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给出，其中 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prerequisites[i] = [a</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">, b</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，表示如果要学习课程 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">a</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">则</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">必须</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">先学习课程 </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">b</font><sub><font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">i</font></sub>`<sub><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font></sub><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">例如，先修课程对 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">[0, 1]</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示：想要学习课程</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">0</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，你需要先完成课程</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">1</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你判断是否可能完成所有课程的学习？如果可以，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

```plain
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736424480886-8a64a6ac-c861-4ab5-91c8-bd13aa7f7c28.png)

```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        edges = collections.defaultdict(list)
        visited = [0] * numCourses
        result = list()
        valid = True

        for info in prerequisites:
            edges[info[1]].append(info[0])
        
        def dfs(u: int):
            nonlocal valid
            visited[u] = 1
            for v in edges[u]:
                if visited[v] == 0:
                    dfs(v)
                    if not valid:
                        return
                elif visited[v] == 1:
                    valid = False
                    return
            visited[u] = 2
            result.append(u)
        
        for i in range(numCourses):
            if valid and not visited[i]:
                dfs(i)
        
        return valid

作者：力扣官方题解
链接：https://leetcode.cn/problems/course-schedule/solutions/359392/ke-cheng-biao-by-leetcode-solution/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

时间复杂度: O(n+m)，其中 n 为课程数，m 为先修课程的要求数。这其实就是对图进行深度优先搜索的时间复杂度。

空间复杂度: O(n+m)。题目中是以列表形式给出的先修课程关系，为了对图进行深度优先搜索，我们需要存储成邻接表的形式，空间复杂度为 O(n+m)。在深度优先搜索的过程中，我们需要最多 O(n) 的栈空间（递归）进行深度优先搜索，因此总空间复杂度为 O(n+m)。



### [<font style="background-color:rgb(240, 240, 240);">实现 Trie (前缀树)（208）</font>](https://leetcode.cn/problems/implement-trie-prefix-tree/)
[**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">Trie</font>**](https://baike.baidu.com/item/%E5%AD%97%E5%85%B8%E6%A0%91/9825209?fr=aladdin)<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（发音类似 "try"）或者说</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">前缀树</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补全和拼写检查。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">请你实现 Trie 类：</font>

+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">Trie()</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">初始化前缀树对象。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">void insert(String word)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">向前缀树中插入字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">boolean search(String word)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">如果字符串</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">在前缀树中，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">（即，在检索之前已经插入）；否则，返回</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。</font>
+ `<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">boolean startsWith(String prefix)</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 如果之前已经插入的字符串 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">word</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 的前缀之一为 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">prefix</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">true</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> ；否则，返回 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">false</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例：</font>**

```plain
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]
```

```python
class Trie:

    def __init__(self):
        self.word_list = []

    def insert(self, word: str) -> None:
        self.word_list.append(word)

    def search(self, word: str) -> bool:
        return word in self.word_list

    def startsWith(self, prefix: str) -> bool:
        for word in self.word_list:
            if len(word) >= len(prefix) and word[:len(prefix)] == prefix:
                return True
        return False
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736476470551-4d685eda-b3f2-4b6f-8d2e-0c4350db5d3e.png)

```python
class Trie:
    def __init__(self):
        self.children = [None] * 26
        self.isEnd = False
    
    def searchPrefix(self, prefix: str) -> "Trie":
        node = self
        for ch in prefix:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                return None
            node = node.children[ch]
        return node

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.isEnd = True

    def search(self, word: str) -> bool:
        node = self.searchPrefix(word)
        return node is not None and node.isEnd

    def startsWith(self, prefix: str) -> bool:
        return self.searchPrefix(prefix) is not None
```

![](https://cdn.nlark.com/yuque/0/2025/png/29769680/1736476508879-ef5aa74c-72c7-43f0-9a9b-8628b3702fb7.png)



### [<font style="background-color:rgb(240, 240, 240);"> 任务调度器（621）</font>](https://leetcode.cn/problems/task-scheduler/)<font style="background-color:rgb(240, 240, 240);">（构造）</font>
<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">给你一个用字符数组 </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">tasks</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">表示的 CPU 需要执行的任务列表，用字母 A 到 Z 表示，以及一个冷却时间</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">。每个周期或时间间隔允许完成一项任务。任务可以按任何顺序完成，但有一个限制：两个</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>****<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">相同种类</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的任务之间必须有长度为</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**`<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>`**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> </font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">的冷却时间。</font>

<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">返回完成所有任务所需要的</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 最短时间间隔</font>**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 。</font>

**<font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">示例 1：</font>**

**<font style="background-color:rgb(240, 240, 240);">输入：</font>**<font style="background-color:rgb(240, 240, 240);">tasks = ["A","A","A","B","B","B"], n = 2</font>

**<font style="background-color:rgb(240, 240, 240);">输出：</font>**<font style="background-color:rgb(240, 240, 240);">8</font>

**<font style="background-color:rgb(240, 240, 240);">解释：</font>**

<font style="background-color:rgb(240, 240, 240);">在完成任务 A 之后，你必须等待两个间隔。对任务 B 来说也是一样。在第 3 个间隔，A 和 B 都不能完成，所以你需要待命。在第 4 个间隔，由于已经经过了 2 个间隔，你可以再次执行 A 任务。</font>

```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        #先考虑最为简单的情况：假设只有一类任务，除了最后一个任务以外，其余任务在安排后均需要增加 n 个单位的冻结时间。
        #将任务数记为 m 个，其中前 m−1 个任务均要消耗 n+1 的单位时间，最后一个任务仅消耗 1 个单位时间，即所需要的时间为 (n+1)×(m−1)+1。

        #当存在多个任务时，由于每一类任务都需要被完成，因此本质上我们最需要考虑的是将数量最大的任务安排掉，其他任务则是间插其中。
        cnts = [0] * 26
        for c in tasks:
            cnts[ord(c) - ord('A')] += 1
        #假设数量最大的任务数为 max，共有 tot 个任务数为 max 的任务种类。
        #实际上，当任务总数不超过 (n+1)×(max−1)+tot 时，我们总能将其他任务插到空闲时间中去，不会引入额外的冻结时间（下左图）；而当任务数超过该值时，我们可以在将其横向添加每个 n+1 块的后面，同时不会引入额外的冻结时间
        maxv, tot = 0, 0
        for i in range(26):
            maxv = max(maxv, cnts[i])
        for i in range(26):
            tot += 1 if maxv == cnts[i] else 0
        #综上，我们所需要的最小时间为上述两种情况中的较大值即可：max(task.length,(n+1)×(max−1)+tot)
        return max(len(tasks), (n + 1) * (maxv - 1) + tot)
```

+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">时间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">n</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">+</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font>
+ <font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">空间复杂度：</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">O</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">(</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">)</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);">，其中 </font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">C</font>_<font style="color:rgba(38, 38, 38, 0.75);background-color:rgb(240, 240, 240);">=26</font><font style="color:rgb(38, 38, 38);background-color:rgb(240, 240, 240);"> 为任务字符集大小</font>

