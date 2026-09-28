# Real-Time Embedded Systems｜即時系統與 RTOS

> 對應 ECEN 5623。重點是 deadline 可分析性，不是單純「速度快」。查核：2026-09-29。模型假設會直接影響結論。

[總覽](README.md) · [專案 P2](Projects.md#p2)

## 目錄

1. [時間模型](#s1)　2. [RM／EDF](#s2)　3. [Response-time analysis](#s3)　4. [同步與阻塞](#s4)　5. [量測與驗證](#s5)　6. [練習與來源](#s6)

<a id="s1"></a>
## 1. 從 deadline 定義開始

Hard real-time：deadline 是正確性的一部分；soft real-time：遲到降低品質。分類看需求，不看用了哪一種 RTOS。影片播放可接受少量 dropped frames，但某控制迴路的容忍度可能不同。

| 記號 | 意義 | 單位 |
| --- | --- | --- |
| C | Worst-case execution time（WCET） | ms 或 µs |
| T | Period；sporadic task 則用最小到達間隔 | 同上 |
| D | Relative deadline | 同上 |
| r | Job release time | 絕對時間 |
| R | Completion − release | 同上 |
| J | Release jitter 界限 | 同上 |
| B | Lower-priority blocking 上界 | 同上 |

WCET 是界限主張；測試中觀察到的最大值只是 observed maximum。Cache miss、interrupt、bus contention、DVFS 都可能使時間變長。先以單核、可搶占、獨立 periodic tasks、D=T、無阻塞與零排程成本建立基礎，再增加真實限制。[R1]

**例 R1：期限與回應。** r=10 ms、D=8 ms，absolute deadline=18 ms。若於 17 ms 完成，R=7 ms、餘裕1 ms；若 task 真正只執行2 ms，其餘5 ms可能是等待與被搶占，不能把 C 與 R 混為一談。

<a id="s2"></a>
## 2. Rate Monotonic 與 Earliest Deadline First

RM 給短週期較高固定優先權。EDF 每次選 absolute deadline 最早的 ready job。兩者都需要明訂同優先序 tie-breaker、release、preemption 與 miss 的處理。

在上述理想模型中，RM 的充分 utilization bound：

$$U=\sum_i C_i/T_i\le n(2^{1/n}-1).$$

超過此界限不代表一定失敗；它是充分條件。EDF 在同一個單核、獨立、可搶占、D=T 理想模型下以 U≤1 判定可排程；若 D<T、有 blocking、jitter、切換成本，不能直接套用。[R1]

**例 R2：通過 RM bound。** 三個 tasks `(C,T)=(1,4),(1,5),(2,10)` ms，U=0.25+0.2+0.2=0.65。三 task bound≈0.77976，因此在假設成立時可排程。到真實 OS 後仍需納入額外成本。

**例 R3：超過 bound 仍可行。** `(1,2),(2,4)`，U=1，高於兩 task bound≈0.8284；但每4 ms：0–1跑A，1–2跑B，2–3跑A，3–4跑B，兩者都準時。Harmonic periods 是一個有利情況。

**公開原論文導讀：** Liu–Layland（1973）§3 列模型假設，§4 討論 fixed priorities，§7 討論 deadline-driven scheduling。先讀假設再看 utilization theorem。這是論文導讀，R2/R3 為自編，不冒充原論文題號。[R1]

<a id="s3"></a>
## 3. Fixed-priority response-time analysis

對這裡採用的單核、可搶占、固定優先權、無 release jitter、constrained deadlines（D≤T）模型，在適用的 bounded-blocking 假設下迭代：

$$R_i^{(k+1)}=C_i+B_i+\sum_{j\in hp(i)}\left\lceil R_i^{(k)}/T_j\right\rceil C_j.$$

由 `C_i+B_i` 開始，若穩定且 ≤D_i 通過；若超過 deadline 即失敗。B_i 必須由實際資源協定得到，不能隨便填0；有 jitter 或 self-suspension 時需另用適合模型。[R2]

**例 R4：算出最低優先權的 response。** 用 R2 的 task set，B=0，task3 從2開始：

| 迭代 | 計算 | 結果 ms |
| --- | --- | --- |
| 0 | C3 | 2 |
| 1 | 2+ceil(2/4)×1+ceil(2/5)×1 | 4 |
| 2 | 2+ceil(4/4)×1+ceil(4/5)×1 | 4 |

所以 R3=4≤10。另兩 task 得1、2 ms。

**例 R5：blocking 會改變結論。** 高優先權 task C=1、D=3 ms，被低優先權不可搶占區段最多阻塞3 ms，僅 C+B=4 ms已超過deadline。降低平均CPU利用率沒有消除這個阻塞。

<a id="s4"></a>
## 4. Task、queue、mutex 與 priority inversion

| 工具 | 目的 | 不應混淆 |
| --- | --- | --- |
| Queue | 傳遞資料與所有權 | 無限 buffer 不存在 |
| Semaphore／notification | 通知事件、計數資源 | 不一定有 owner／priority inheritance |
| Mutex | 保護共享不變量 | 一般不能在 ISR 中阻塞取得 |
| Atomic operation | 特定操作不可分割 | 多個 atomic 不自動形成交易 |

Priority inversion：低優先權L持有鎖，高優先權H等待；中優先權M反覆搶占L，間接延誤H。Priority inheritance 可暫時提高L讓它釋放鎖，但不保證沒有 deadlock，也不等於零 blocking。FreeRTOS 的 mutex 有其具體且簡化的繼承行為，必須看所用版本；binary semaphore 不等同 mutex。[R3]

**例 R6：死鎖。** Task A 持有 bus_lock 等 log_lock；Task B 持有 log_lock 等 bus_lock。兩者皆無法前進。規定所有執行者皆先取 bus_lock 再取 log_lock，可去除這個循環等待；仍需檢查其他鎖與持有時間。

把 blocking I/O 移出持鎖區通常比盲目提高優先權有效。需要 snapshot 時，在鎖內複製必要資料，放鎖後寫檔。不能只為縮短鎖而把一致性需求移除。

### 4.1 Periodic work 的實作概念

```
next_release = monotonic_now()
repeat:
    next_release += period
    do_bounded_work()
    wait_until(next_release)
```

這是 pseudocode。若已錯過 next_release，要明訂 catch-up、skip 或 report miss；不能任由無限補工作讓系統失控。牆上時鐘可能受校時改變，測量間隔優先使用 monotonic clock。

<a id="s5"></a>
## 5. 模擬、RTOS 與 host 實驗的界線

先寫 discrete-event／整數 tick 模擬器，在同一輸入下比較 RM/EDF。這可揭露模型裡的 deadline miss，不能證明 macOS 有 hard real-time 保證。Linux VM 的實際 thread timing 同樣受 host 干擾。

Zephyr `native_sim` 產生 Linux executable，不是原生 macOS target，也不模擬指定 MCU；其 virtual time 和 wall time 可以不同。M2 先做純 Python 排程模型；RTOS Linux target 的架構支援在實作時確認。[R4]

**例 R7：buffer sizing。** 200 samples/s，worker 停頓0.25s，會累積約50 samples。若每筆16 bytes，資料本身800 bytes；64筆queue的payload為1024 bytes，但還有metadata。恢復服務率若400/s，淨清除速率200/s，50筆約再需0.25s。

報告至少記錄：hardware／VM／OS、clock來源、負載、樣本數、min／median／p99／max與miss count。不把一次量測 p99 當成 WCET；不將虛擬時間deadline說成板級結果。

<a id="s6"></a>
## 6. 練習與解答

1. `(C,T)=(1,5),(2,10)` 的 U 與最低優先權 R？
2. 若deadline改為2 ms但period10 ms，U不變是否仍能用 EDF U≤1 結論？
3. 能用 mutex 解決 circular wait 的全部問題嗎？
4. 觀測一百萬次沒有miss，能保證第1000001次嗎？

<details><summary>解答</summary>

1. U=0.4；R初值2→3→3，通過 D=10。
2. 不能；D=T假設已破壞，需 demand analysis 或適用分析。對此例還需檢查具體排程。
3. Mutex 提供排他，不自動避免死鎖；需鎖順序、協定與持有時間分析。
4. 不行。這是測試證據，還要有覆蓋、界限與模型論證。

</details>

| ID | 來源 | 閱讀方向 |
| --- | --- | --- |
| R1 | [Liu & Layland, 1973 原論文](https://www.cs.ru.nl/~hooman/DES/liu-layland.pdf) | 假設、RM、deadline-driven scheduling |
| R2 | [Baruah／Burns／Davis, RTSS2011作者投影片](https://www-users.york.ac.uk/~rd17/papers/RTSS2011_MC_slides.pdf) | 第11頁single-criticality的B=0 recurrence；本文B項另須符合bounded-blocking模型 |
| R3 | [FreeRTOS mutex 文件](https://freertos.org/Real-time-embedded-RTOS-mutexes.html) | Priority inheritance 與使用限制 |
| R4 | [Zephyr native_sim](https://docs.zephyrproject.org/latest/boards/native/native_sim/doc/index.html) | 模擬時間、Linux host 與限制 |

`examples/check_models.py` 重算 R2–R4；P2 完整排程工具為 planned。
