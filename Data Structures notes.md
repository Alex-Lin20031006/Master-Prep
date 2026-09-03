# Data Structures（資料結構學習筆記）
### 1.  What is Data Structure
  在電腦世界裡，資料結構就是程式設計師在記憶體裡蓋的書架。
### 2.  什麼是Big O 複雜度
  並不使用秒數來測速，而是看「**當資料量變多時，步驟增加了多少**」。這就是**Big O Notation** 。<br>
  以下為最常見的三種基礎速度：<br>
  >1.  O(1)：瞬間完成（不管多少筆資料都只需要一個步驟）
  >2.  O(n)：慢慢變長（步驟跟資料量成正比）
  >3.  O(logn)：砍半尋找（每次找不對，就把剩下的資料砍一半)<br>
  
  >[!NOTE]
  >Type 3.  舉例來說，猜數字1-100。你猜50，我說太大，就直接排除50-100。（速度極快）
### 3.  Array v.s. Linked List
  1.  Array:<br>
  >連續的格子：記憶體裡包下一整排連續、緊鄰的房間。

  >[!NOTE]
  >＊特性：每個房間都有號碼牌（索引，從0開始）<br>
  >＊優點：找特定房間的人非常快<br>
  >＊缺點：大小固定、中間插隊很痛苦（有人插隊，後面的人都要往後挪。O(n)複雜度）<br>
  2.  Linked List:<br>
  >房間不一定連續，每個人住不同的地方，但手上有紙條寫著下一個住在哪一間。

  >[!NOTE]
  >＊特性：每個節點(node)包含「資料」和「指向下一個人的指標(pointer)」<br>
  >＊優點：要多少有多少、插隊很方便（O(1)複雜度）<br>
  >＊缺點：找人很慢（O(n)複雜度）<br>
#### 實作一：動態陣列(Dynamic Array)
1.  Python
```python
#initial an empty dynamic array
arr=[]

#append
arr.append(10)
arr.append(20)
arr.append(30)

#print
print(arr)
print(arr[0])
```
2.  C++
```c++
#include <iostream>
#include <vector>
using namespace std;

int main()
{
    //initial an empty dynamic array
    vector<int>vec;
    
    //append
    vec.push_back(10);
    vec.push_back(20);
    vec.push_back(30);
    
    //print
    for(int num:vec){
        cout<<num<<" ";
    }
    cout<<"\n"<<vec[]<<"\n";
    
    return 0;
}
```
>[!NOTE]
>兩個程式碼會產生一模一樣的結果
#### 實作二：串列結構(Linked List)
因為串列結構是一環扣一環的，要先定義一個節點(node)長怎樣。每個節點都要有：<br>
- 資料(Data)<br>
* 下一個人的地址(Next指標/引用)<br>
1.  Python
```python
#define a node's blueprint
class Node:
    def __init__(self,data):
        self.data=data  #save data
        self.next=None  #sve next node, initially set as none

#define 3 independent nodes
node1=Node(10)
node2=Node(20)
node3=Node(30)

#connect
node1.next=node2  #node1 points to node2
node2.next=node3

#print
current=node1
while current is not None:
    print(current.data)
    current=current.next
print("End")
```
2.  C++
```c++

```
###
