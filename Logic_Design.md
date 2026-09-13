# Logic Design
## CH0 Concepts
- `Analog`: Continuously varying signal
- `Core of Digital Logic`: Using simple discrete states to represent and process information
- `Truth Table`: Shows what output is produced for every combination of inputs
>[!IMPORTANT]
>- n binary inputs → $2^n$ possible combinations

>[!TIP]
>- `AND`: Evaluates to true only when all inputs are true
>- `OR`: Evaluates to true if at least one input is true
>- `NOT`: Takes only one input and outputs its inverse
## CH1 Number Systems
#### CH1-1 Terminology and Key Concepts
- `Decimal`: Base-10 system (used in daily life)
- `Binary`: Base-2 system
- `Binary Representation`: $1011_2$ (written as a subscript)
>[!NOTE]
>Ex:<br>
>$1011_2$ = $1(2^3)+0(2^2)+1(2^1)+1(2^0)$ = $11_{10}$

- `bit (Binary Digit)`: A single binary digit
>[!TIP]
>- 1 bit → 2 states (can be 0 or 1)<br>
>- n bits → $2^n$ possible values<br>
>- Unsigned range for n bits = 0~ $(2^n -1)$

- `Hexadecimal`: Base-16 system
>[!TIP]
>- Elements: 0-9 and A-F (where A=10, B=11, C=12, D=13, E=14, F=15)
>- Representation: Commonly indicated by a subscript $n_{16}$ or $n_{hex}$, or prefixed with `0x`.
> - Examples:
>      - Mathematical notation: $A3F_{16}$ or $2C_{16}$
>      - Code notation: `0x2C` (more commonly used in web and programming)

>[!IMPORTANT]
>- 1 Hex digit corresponds exactly to 4 Binary bits
>- Ex: $10101111_2 = AF_{16}$ <br>
> ```text
> 1010    1111
>  ↓        ↓
>  A        F
> ```
>---
>- If the number of bits is not a multiple of 4, pad with leading 0s to the left
>- Ex: $101101_2 = 2D_{16}$ <br>
> ```text
> 0010    1101
>  ↓        ↓
>  2        D
> ```

- `Byte`: 8 bits
#### CH1-2 Binary Addition
Binary Addition:
| A | B | RESULT |
| :-: | :-: | :-: |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 10 |
>[!IMPORTANT]
>- $1+1 = 10_2$

>[!NOTE]
>Ex:<br>
>$1011_2 +0110_2 =?$<br>
>```text
>   1011
> + 0110
> ------
>  10001
>```
>Ans: $10001_2 = 17$
#### CH1-3 Introduction to Adders
- $1+1=10_2$ , which means:
  - $Sum=0$
  - $Carry=1$
- A Half Adder can perform the following:
  ```text
  A ──┐
      │
      ├── Half Adder ── Sum
      │
  B ──┘               └─ Carry
  ```
>[!TIP]
>Its core logic is:
>  - $Sum = A \oplus B$
>  - $Carry = AB$

#### CH1-4 Leading Zeros
- $1011_2$ and $00001011_2$ represent the same numerical value.
- This is standard in computers and is known as **8-bit representation**.

#### CH1-5 Knowledge Map (Chapter 1-1 ~ 1-4 Summary)
```text
                 Number System
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Decimal      Binary       Hex
       Base 10      Base 2      Base 16
          │           │           │
          │           │           │
          └────── Conversion ─────┘
                      │
                      ↓
                     Bits
                      │
                      ↓
                Binary Arithmetic
                      │
                      ↓
                  Logic Gates
                      │
                      ↓
                    Adders
                      │
                      ↓
                     ALU
```

#### CH1-6
#### CH1-7
## CH2 Boolean Algebra
## CH3 Boolean Expressions
## CH4 Combinational Logic
## CH5 Sequential Logic
## CH6 Registers and Counters
## CH7 Finite State Machine
## CH8 Memory and Digital Systems
## CH9 Advanced Digital Design
