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
>[!TIP]
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
#include <iostream>
using namespace std;

struct Node{
    int data;   //save the data
    Node* next; //pointer to the next node

    Node(int val): data(val), next(nullptr) {} //constructor to initialize the node
};

int main(){
    //create 3 nodes in heap memory(堆積記憶體) 
    Node* node1=new Node(10); //create a new node with data 10
    Node* node2=new Node(20); 
    Node* node3=new Node(30); 

    //用指標串起來
    node1->next=node2;  //node1's next points to node2
    node2->next=node3;

    //print the linked list
    Node* current=node1;
    while(current!=nullptr){ //while current is not null
        cout<<current->data<<" -> ";
        current=current->next;
    }
    cout<<"nullptr(end)"<<endl;

    //delete the nodes to free memory
    delete node1;
    delete node2;
    delete node3;

    return 0;
}
```
>[!NOTE]
>程式運作邏輯：不管是Python或C++，要找到最後一個節點，都必須使用while迴圈從頭找。這就是Linked List 尋找資料要O(n)的時間。
#### 實作三：Linked List 的「中間插隊」
假設目前的串列是：10 -> 30。現在要在中間插入一個20，變成10 -> 20 -> 30。
1.  Python
```python
class Node:
    def __init__(self,data):
        self.data=data
        self.next=None

#建立初始
node1=Node(10)
node3=Node(30)
node1.next=node3

print("Initial")
def print_list(head):
  curr=head
  while curr:
    print(curr.data, end=" -> ")
    curr=curr.next
  print("None")

print_list(node1)

#開始插隊
node2=Node(20)
node2.next=node1.next
node1.next=node2

print("\nAfter insertion")
print_list(node1)
```
２.  C++
```c++
#include <iostream>
using namespace std;

struct Node{
    int data;   //save the data
    Node* next; //pointer to the next node

    Node(int val): data(val), next(nullptr) {} //constructor to initialize the node
};

void printList(Node* head){
    Node* current=head;
    while(current!=nullptr){ //while current is not null
        cout<<current->data<<" -> ";
        current=current->next;
    }
    cout<<"nullptr(end)"<<endl;
}

int main(){
    //initial
    Node* node1=new Node(10); //create a new node with data 10
    Node* node3=new Node(30);
    node1->next=node3;

    cout<<"Initial linked list: ";
    printList(node1);

    //開始插隊
    Node* node2=new Node(20);
    node2->next=node1->next;
    node1->next=node2;

    cout<<"Linked list after insertion: ";
    printList(node1);

    //delete the nodes to free memory
    delete node1;
    delete node2;
    delete node3;

    return 0;
}
```
### 4.  Stack與Queue
這兩個是非常經典的「抽象（行為規則）資料型態」，底層可以用Array或Linked List來實作都可以。<br>
1.  Stack - 後進先出(LIFO)<br>
- 專有名詞：<br>
  - Push：把資料放進堆疊頂端<br>
  * Pop：把堆疊頂堆的資料拿走<br>
* 應用：瀏覽器的「上一頁」功能
2.  Queue - 先進先出(FIFO)<br>
- 專有名詞：<br>
  - Enqueue(Push)：把資料加入隊伍尾端<br>
  * Dequeue(Pop)：把隊伍最前端的資料拿走<br>
* 應用：印表機的工作排隊（先送出的文件先印）、封包傳輸
#### 實作：Stack和Queue
現代開發中，很少需要從頭寫這兩種資料型態的實作，因為程式語言的標準庫都內建好了。<br>
1.  Python：在Python中，list可以直接當成stack使用；而queue則推薦使用collections.dequeue
```python
from collections import deque

#Stack
stack=[]
stack.append("plate A")
stack.append("plate B")
stack.append("plate C")#last in
print("Stack Pop:", stack.pop())#first out

#Queue
queue=deque()
queue.append("customer A")#first in
queue.append("customer B")
queue.append("customer C")
print("Queue Dequeue:", queue.popleft())#first out
```
2.  C++：STL直接提供了stack與queue
```c++
#include <iostream>
#include <stack>
#include <queue>
using namespace std;

int main(){
    //stack
    stack<string> s;
    s.push("plate A");
    s.push("plate B");
    s.push("plate C");
    cout<<"Top of stack: "<<s.top()<<endl; //C
    s.pop();
    cout<<"Top of stack after pop: "<<s.top()<<endl; //B

    //queue
    queue<string> q;
    q.push("customer A");
    q.push("customer B");
    q.push("customer C");
    cout<<"Front of queue: "<<q.front()<<endl; //customer A
    q.pop();
    cout<<"Front of queue after pop: "<<q.front()<<endl; //customer B

    return 0;
}
```
### 5.  雜湊表（Hash Table/ Map）
1.  核心原理：
- Bucket（桶子/陣列）：底層為一個大陣列，用來儲存資料。
- Hash Function（雜湊函數）：給一個Key（字串、物件都行），透過數學公式，算出來一個整數索引（Index）。
>Example：<br>
>Input "Alice" -> 經過雜湊函數算出數字3 -> 把Alice存入陣列第3個格子<br>
>下次查詢 "Alice" -> 再算一次得到3 -> 直接讀取第3個格子<br>
- 雜湊碰撞（Hash Collision）：如果兩個資料算到同一格子時。
>[!IMPORTANT]
>解決方法：
>  - Chaining（鏈結法）：每個格子不只存一個人，而是掛一條Linked List。
>  - Open Addressing（開放地址法）：往下一個格子尋找是否是空格子，又叫作線性探測（Linear Probing）。
#### 實作：雜湊表
1.  python：在Python中叫dict
```python
#python的dict底層就是高度優化的雜湊表
phone_book={}

#insert data
phone_book["Alice"]="0911-111-111"
phone_book["Bob"]="0922-222-222"

#search data
print("Alice's Phone: ",phone_book["Alice"])

#check key
if "Charlie" in phone_book:
    print("Charlie is in the phone book.")
else:
    print("Charlie is not in the phone book.")
```
2.  C++：叫unordered_map
```c++
#include <iostream>
#include <unordered_map>
#include <string>
using namespace std;

int main(){
    unordered_map<string, string> phonebook;

    //insert
    phonebook["Alice"] = "0911-111-111";
    phonebook["Bob"] = "0922-222-222";

    //search
    cout<<"Alice's phone number: "<<phonebook["Alice"]<<endl; //0911-111-111

    //check key existence
    if(phonebook.find("Charlie") != phonebook.end()){
        cout<<"Find Charlie's phone number."<<endl;
    } else {
        cout<<"Charlie is not in the phonebook."<<endl;
    }

    return 0;
}
```
>[!TIP]
>```c++
>phonebook.end()
>```
>回傳的是指向雜湊表（或任何一個容器）最後一個元素後面的虛擬位置指標（迭代器 Iterator），在程式碼中扮演「找不到的終點線」
>```c++
>phonebook.begin()
>```
>指向第一個有效的資料
### 6.  樹狀結構（Tree）
1.  專有名詞
- Root（根節點）：最頂端的起點（只有一個）
- Node（節點）：樹裡面的每一個資料元素
- Parent/Child（父節點/子節點）：上下的連接關係
- Leaf（葉節點）：最底層、沒有任何子節點的尾端
2.  核心：二元搜尋樹
- 限制一：每個節點最多只能有兩個小孩
- 限制二：左邊所有小孩的值，都必須小於自己；右邊所有小孩的值，都必須大於自己
>Example：想在樹裡找18<br>
>Step1：先看根節點是15（18>15），所以左邊全部不用看了，看右邊就好<br>
>Step2：右邊節點是20（18<20），所以右邊全部不用看了，看左邊就好<br>
>Step3：找到18（每次比對都直接砍掉一半的可能性）<br>
#### 實作：二元搜尋樹
手寫樹狀結構會需要使用到座標/引用。手寫一個節點，建立小樹
1.  Python
```python
#定義樹的節點
class TreeNode:
    def __init__(self,value):
        self.value=value
        self.left=None  #left child
        self.right=None #right child
  
#寫一個函數來計算樹的最大深度
def get_max_depth(root):
    if root is None:
        return 0
    #遞迴計算左子樹與右子樹的深度取最大，再加上自己這一層
    return max(get_max_depth(root.left),get_max_depth(root.right))+1

#寫一個前序走訪（根 -> 左 -> 右），把所有號碼印出來
def pre_order_print(root):
  if root:
    print(root.value, end=" ")
    pre_order_print(root.left)
    pre_order_print(root.right)


#蓋一顆二元搜尋樹
root=TreeNode(1)

#floor 2
root.left=TreeNode(2)
root.right=TreeNode(3)
#floor 3
root.left.left=TreeNode(4)
root.left.right=TreeNode(5)
root.right.left=TreeNode(6)
root.right.right=TreeNode(7)
#floor 4
root.left.left.left=TreeNode(8)
root.left.left.right=TreeNode(9)
root.left.right.left=TreeNode(10)
root.left.right.right=TreeNode(11)

root.right.left.left=TreeNode(12)
root.right.left.right=TreeNode(13)
root.right.right.left=TreeNode(14)
root.right.right.right=TreeNode(15)

#result
print("Python Tree Test")
print(f"The floors(deepth) of this tree are {get_max_depth(root)} floors.")
print("The visit order:")
pre_order_print(root)
print()
```
2.  C++
```c++

```
3.  C++
### 7.
### 8.

