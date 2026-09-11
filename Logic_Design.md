# Logic Design
## CH0 Concepts
- `Analog（類比訊號）`：連續變化的訊號
- `數位邏輯的核心`：使用簡單的離散狀態來表示、處理資訊
- `Truth Table（真值表）`：每一種輸入組合會產生什麼輸出
>[!IMPORTANT]
>- n 個 binary inputs → $2^n$種可能組合

>[!TIP]
>- `AND`：全部符合成立
>- `OR`：一個符合就成立
>- `NOT`：只有一個input，輸出為反向
## CH1 Number Systems
#### CH1-1 名詞
- `Decimal`（Base 10）：十進位（日常使用）
- `Hexadecimal`：十六進位
>[!TIP]
>- 組成元素：0-9 和 A-F (其中 A=10, B=11, C=12, D=13, E=14, F=15)
>- 進位標示：通常在右下角加上 $n_{16}$ 或 $n_{hex}$，或者在前方加上 `0x`。
> - 表示範例：
>     - 數學標記法： $A3F_{16}$ 或 $2C_{16}$
>     - 程式碼標記法：`0x2C` (在網頁或程式中更常用)

- `Binary`（Base 2）：二進位
- `二進位表示法`： $1011_2$ （寫在右下角）
>[!NOTE]
>EX:<br>
>$1011_2$ = $1(2^3)+0(2^2)+1(2^1)+1(2^0)$ = $11_{10}$

- `bit（Binary Digit）`：一個二進位數字
>[!TIP]
>- 1 bit → 2 states（可能是0或1）<br>
>- n bits → $2^n$ possible values<br>
>- n bits 的 unsigned range = 0~ $(2^n -1)$

>[!IMPORTANT]
>- 1 個 Hex digit 剛好代表 4 個 Binary bits
>- Ex： $10101111_2 = AF_{16}$ <br>
> ```text
> 1010    1111
>  ↓        ↓
>  A        F
> ```
>---
>- 如果不足4的倍數，往左邊補0
>- Ex： $101101_2 = 2D_{16}$ <br>
> ```text
> 0010    1101
>  ↓        ↓
>  2        D
> ```

- `Byte`：8 bits
#### CH1-2
Binary Addition：
#### CH1-3
#### CH1-4
#### CH1-5
#### CH1-6
#### CH1-7
## CH2 Boolean Algebra
## CH3 Boolean Expression
## CH4 Combinational Logic
## CH5 Sequential Logic
## CH6 Registers and Counters
## CH7 Finite State Machine
## CH8 Memory and Digital Systems
## CH9 Advanced Digital Design
