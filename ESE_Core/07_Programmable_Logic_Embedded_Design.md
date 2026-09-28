# Programmable Logic Embedded System Design｜FPGA 與可程式邏輯

> 對應 ECEN 5863；接續 [Logic Design](../Logic_Design.md)，從RTL進入可驗證的資料路徑、FIFO與時序。查核：2026-09-29。未將尚未開設／未核實的Advanced Programmable Logic課程冒稱已完整覆蓋。

[總覽](README.md) · [P7](Projects.md#p7)

## 目錄

1. [FPGA與RTL](#s1)　2. [位寬與時序](#s2)　3. [介面與FIFO](#s3)　4. [CDC與reset](#s4)　5. [驗證流程](#s5)　6. [練習與來源](#s6)

<a id="s1"></a>
## 1. Hardware description不是順序軟體

FPGA包含LUT、flip-flops、routing及器件特定RAM／DSP等資源。RTL描述每cycle的register transfer與組合邏輯；多個process同時活動。Synthesis把可合成描述轉為硬體netlist，不是把任意程式變成高速CPU程式。

| 寫法 | 意義 | 常見問題 |
| --- | --- | --- |
| `always_comb` | 組合邏輯 | 少賦值造成非預期latch／工具警告 |
| `always_ff @(posedge clk)` | Clocked registers | Nonblocking時看到的是更新前值 |
| `for` 固定迭代 | 可能展開多份硬體 | 不是免費的多cycle運算 |
| `#delay` | 模擬時間控制 | 不當成可攜帶的硬體延遲元件 |

正式course page說明器件與工具方向；本筆記以SystemVerilog作可讀範例，並不聲稱當期課堂一定使用相同HDL。[F1][F2]

**例 F1：pipeline與nonblocking。** `a<=in; b<=a;`在同個edge時b取得舊a。假設初始a=b=0，输入依序3、5、7，edge後(a,b)依序(3,0)、(5,3)、(7,5)。這是兩級register，不是先把a變新值再讓b立即跟上。

<a id="s2"></a>
## 2. 位寬、signedness與pipeline

**例 F2：sum寬度。** 八個unsigned12-bit數最大8×4095=32760，需15bits。若保留每級加法結果的位寬不足，即使最後變數15bits也可能太晚；運算前明確延伸。

**例 F3：fixed point。** 本題signed16-bit、fractional bits=8，數值=stored_integer/256。1.5編碼384，−0.25編碼−64。相乘整數結果−24576，fractional bits=16，真值−0.375。轉回8 fractional bits需定義rounding與saturation；直接右移的負數捨入方向不一定等於toward-zero。

單一路徑忽略skew時setup要求：`Tclk ≥ tCQ,max + tlogic,max + tsetup`。Hold用min delay檢查，不能藉降低頻率修正。真實STA另計clock uncertainty、skew、I/O constraints與多時脈關係。

**例 F4：pipeline取捨。** 原組合path9ns，CQ0.4ns、setup0.6ns，period≥10ns。分成三段各3ns並加register，period≥4ns，理論250MHz。但clock latency增加，需讓data與valid同步延遲；最大frequency與每筆end-to-end latency不是同一件事。

<a id="s3"></a>
## 3. Ready/valid與FIFO

在指定的上升edge，只有ready&&valid才轉移一筆。當valid=1、ready=0時，source需保持payload與valid直到被接受（依本協定）；sink可backpressure。不要在每個valid cycle都計數，否則stall時重複消費。

**例 F5：握手追蹤。** 連續四個edge，valid=[1,1,1,0]、ready=[0,0,1,1]，只有第三個edge成功一次。前三個edge看到的payload必須一致；這是資料穩定性測試的重點。

同步FIFO以共同clock讀寫。Full／empty、同cyclepush+pop、reset與overflow策略都需明訂。Depth=16不代表永遠保證16個burst可吸收，還要看初始occupancy與同時pop。

**例 F6：FIFO容量。** 每cycle最多寫1筆，consumer最長連續停12cycles；若初始已有3筆、且停頓期間producer持續送，occupancy可到15，depth16僅剩1格。若用保留一格的ring表示，物理16格可能只允許15筆，界限剛好滿。

### 3.1 CPU與FPGA協作

Memory-mapped registers通常分control、status、data；長資料可用stream與DMA。CPU寫start後讀status需要定義busy、done清除方式與錯誤。硬體IP與軟體driver若對「寫1清除」理解不同，integration可能失敗。先用testbench模擬software操作sequence，再接真實bus。

<a id="s4"></a>
## 4. Clock domain crossing與reset

單bit慢變level可考慮多級synchronizer；短pulse可能被漏掉，需要toggle／handshake等方案。多bit關聯資料不能每bit獨立同步後就當一致word；常用handshake或async FIFO。Gray pointer也需要正確CDC結構、物理約束與設計假設，不是萬用免死金牌。[F3]

**例 F7：漏pulse。** Destination clock每20ns取樣，source pulse僅5ns，若落在兩個destination edges之間，兩級FF也可能完全看不到。兩級FF改善metastability propagation機率，不是pulse stretcher。

Reset需要定義polarity、同步／非同步、解除時序與各domain啟動順序。若FIFO兩端不同時間reset，必須考慮資料丟棄與重新同步的協定。Simulation通常不會模擬真實analog metastability。

<a id="s5"></a>
## 5. 從spec到testbench與STA

| 階段 | 產物 | 可以主張 |
| --- | --- | --- |
| Spec／reference model | 位元精確輸入輸出 | 預期行為已定義 |
| RTL simulation | 可重現test vectors、assertions | 被覆蓋情境的RTL行為 |
| Synthesis | 資源報告、warnings | 工具可映射至特定target |
| Place and route／STA | Clocks、I/O constraints、timing report | 在約束與模型下的timing結果 |
| Hardware test | Waveform、board條件 | 已量測情境的實體行為 |

**例 F8：reference對照。** 設計unsigned8-bit saturating adder，golden model=`min(a+b,255)`。共有65536組輸入，全部可窮舉。另測valid stall、reset與pipeline對齊；只比最終sum不能檢查時序協定。

Mac可先用Verilator做RTL simulation／lint；官方提供macOS安裝途徑。這不表示Vivado／Quartus bitstream流程原生支持M2，正式板級工具可能需校方或遠端支持環境。[F4]

建議P7先做saturating adder→ready/valid→synchronous FIFO→UART或PWM延伸。不要第一次就同時寫async FIFO、AXI與自製CPU。

### 公開教材例題導讀

回到Logic Design中Plantz Chapter5 Example5-a的enabled counter，觀察「next-state推導」如何轉成clocked RTL。這是已標示來源的公開例子；F1–F8為新編教科書型例題。驗證方法參考工具文件，不冒稱工具手冊提供所有原題。

<a id="s6"></a>
## 6. 練習

1. 16個unsigned10-bit相加需要多少bits？
2. valid為1但ready為0連續5cycles，成功傳幾筆？
3. 100MHz時每1000cycles產生tick，tick rate與toggle方波頻率？
4. RTL simulation沒有X是否表示實機無metastability？

<details><summary>解答</summary>

1. 最大16368，14bits。
2. 0筆；仍需保持pending payload。
3. Tick=100kHz，若每tick toggle，方波=50kHz。
4. 否，數位RTL模型未表達analog metastability的完整物理行為。

</details>

| ID | 來源 | 用途 |
| --- | --- | --- |
| F1 | [ECEN5863公開頁](https://sites.google.com/colorado.edu/ecen5863) | 課程方向；歷史頁不當作2027工具保證 |
| F2 | [AMD UG901 Always Procedures](https://docs.amd.com/r/2023.2-English/ug901-vivado-synthesis/Always-Procedures) | RTL process與synthesis語義 |
| F3 | [AMD UG949 CDC](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Clock-Domain-Crossing) | CDC工程檢查方向 |
| F4 | [Verilator installation](https://verilator.org/guide/latest/install.html) | macOS simulation工具入口 |
| F5 | [Plantz Chapter5](https://bob.cs.sonoma.edu/IntroCompOrg-x64/bookch5.html) | Example5-a公開原例導讀 |

本次驗證reference arithmetic，沒有宣稱執行新的RTL、合成或STA；P7實作為planned。
