# Embedded System Design｜嵌入式系統設計

## 入門導讀｜從計算到實體設備

先讀 [共通基礎](../Foundations.md)。嵌入式設計關心「輸入從哪來、何時處理、結果如何作用於外界、出錯如何恢復」。智慧洗衣機、鍵盤與汽車控制器都共享這個架構，但不一定使用同一種晶片或作業系統。

| 名詞 | 白話與用途 |
| --- | --- |
| MCU, microcontroller 微控制器 | 把 CPU、記憶體與控制週邊整合在一起的晶片 |
| SBC, single-board computer 單板電腦 | 在一塊板子上組成可運作的電腦；常可執行完整 OS |
| SoC, system-on-chip | 在晶片內整合多種系統功能；分類與 MCU 有交集 |
| GPIO | 可由程式讀取或輸出的通用數位接腳 |
| MMIO, memory-mapped I/O | 用特定位址讀寫來操作週邊 |
| Register 寄存器 | 此處指週邊內的設定或狀態欄位，不是一般 RAM |
| Flag 旗標 | 表示某個條件或事件的一個位元 |
| Mask 遮罩 | 用 1 標出要操作的位元位置 |
| ISR | 中斷服務常式：回應硬體中斷時執行的函式 |
| DMA | 專用硬體依設定搬資料，減少 CPU 逐筆搬運 |
| Watchdog 看門狗 | 未在期限內得到預期服務時觸發恢復的機制 |

### 必懂例子：read-to-clear 與 write-one-to-clear

讀取 read 是向裝置要求回傳資料；寫入 write 是送一個值給裝置。**clear 指把旗標清成 0**；不是刪除程式碼，也不一定是清除資料 buffer。週邊可以把讀寫解釋成「命令」，不能一律當成普通變數賦值。

| 存取類型 | 讀取做什麼 | 寫入做什麼 |
| --- | --- | --- |
| 一般 R/W | 回傳目前值 | 用寫入值更新欄位 |
| RO, read-only | 回傳目前狀態 | 不能當作可寫欄位使用 |
| RC, read-to-clear | 回傳狀態後清除指定旗標 | 依器件規格；不要自行假設 |
| W1C, write-one-to-clear | 是否可讀須看欄位規格 | 寫 1 清該位，寫 0 不改該位 |
| W1S, write-one-to-set | 是否可讀須看欄位規格 | 寫 1 設該位，寫 0 不改該位 |

**自編逐步例題：** 假設三個純 W1C 旗標目前是 `101`，bit 2 和 bit 0 都有事件。只想確認 bit 0 已處理，寫 `001`，結果為 `100`。若寫 `000`，仍是 `101`。不要用一般變數的「寫 0 就清除」直覺。

| 操作前 | 操作 | 回傳／送出值 | 操作後（假設無新事件） |
| --- | --- | --- | --- |
| RC 狀態 101 | 第一次讀 | 回傳 101 | 000 |
| RC 狀態 000 | 第二次讀 | 回傳 000 | 000 |
| W1C 狀態 101 | 寫 001 | 只確認 bit 0 | 100 |
| W1C 狀態 101 | 先讀再 OR 001 寫回 | 寫出 101 | 000：兩個都被清除 |

> [!WARNING]
> `STATUS |= mask` 是「讀、OR、再寫」三個概念步驟，可能把其他已為 1 的 W1C 旗標也清掉。除錯器自動刷新寄存器視窗也可能讀到 RC 寄存器並造成清除。實際還要查保留位、讀寫寬度與事件同時發生的優先規則。

純 W1C 且手冊允許時，概念操作是直接寫欲清除的 mask；混合 R/W、W1C 或保留位的寄存器不能照抄。上述是教學模型，不提供任何晶片實體位址。定義核對 [Microchip Register Bit Types](https://onlinedocs.microchip.com/oxy/GUID-7A87AF7C-8456-416F-A89B-41F172C54117-en-US-10/GUID-28A3C34B-707C-4315-8908-0B68D7C5BE72.html) 與 [Arm CMSIS-SVD register semantics](https://arm-software.github.io/CMSIS_5/SVD/html/elem_registers.html)。

### 不同資料搬運方法怎麼想

Polling 是你一直查看收件匣；interrupt 是新信觸發通知；DMA 是先設定搬運清單，由另一個硬體單元搬資料。三者可搭配使用。中斷不是「任何時候都立刻完成」，還受遮罩、優先序與處理時間影響。

> [!TIP]
> 讀資料手冊時依序找：位址、寬度、reset value、每個欄位的意義、存取屬性、必要操作順序。先用紙筆寫出一次讀寫前後的狀態，再寫程式。
> [!NOTE]
> 本篇按領域概念組織，從基礎走向進階；課程代碼不代表先備要求。原有來源與例題保留供第二輪深入閱讀。

[學習總覽](README.md) · [共通基礎](../Foundations.md) · [邏輯先修](../Logic_Design.md)

## 目錄

1. [需求與架構](#s1)
2. [CPU、記憶體與開機](#s2)
3. [GPIO、匯流排與時間](#s3)
4. [中斷、DMA 與事件](#s4)
5. [FSM 與故障設計](#s5)
6. [整合、練習與來源](#s6)

<a id="s1"></a>

## 1. 先寫出可驗收的需求

嵌入式系統把計算嵌入實體環境；成功條件通常同時包含正確輸出、期限、耗能、成本與可恢復性。溫度資料最後算對，但風扇晚開十秒，仍可能不合規格。[D1]

| 需求層次 | 模糊說法 | 可測試的自訂規格 |
| --- | --- | --- |
| 功能 | 能讀溫度 | 每 100 ms 接受一筆帶序號樣本 |
| 時間 | 警報很快 | 已接受的高溫樣本在 20 ms 內更新狀態 |
| 故障 | 不會當掉 | 缺資料超過 500 ms 進入 SENSOR_FAULT |
| 資源 | 記憶體很少 | 固定大小 32 筆 queue，滿時記錄 dropped counter |
| 證據 | 測試成功 | 保存輸入、預期狀態、實際狀態與測試版本 |

注意「物理變化到警報」還包含感測器反應與取樣等待，不能和「樣本接受後的期限」混用。以下數值皆為自編教科書型例題，不是產品建議值。

**例 E1：延遲預算。** 每 100 ms 取樣，感測器轉換 8 ms，queue 最壞等待 3 ms，運算 2 ms，輸出 1 ms。若變化剛好發生在上次取樣之後，最壞延遲上界約 114 ms。需求若為 50 ms，不能只把 2 ms 的演算法加快：取樣週期本身已經太長。把週期改為 20 ms，其他條件不變，上界為 34 ms。此加總假設各延遲串接、且界限已成立；共享資源阻塞須另計。

### 1.1 MCU、SBC 與 FPGA

| 平台 | 擅長 | 需要注意 |
| --- | --- | --- |
| MCU | 控制、低功耗、週邊與中斷 | RAM 小、需研究 datasheet |
| Linux SBC | 網路、檔案、複雜應用 | OS 排程與儲存會增加時間變動 |
| FPGA | 平行資料路徑、精確 clock 行為 | HDL、時序約束與硬體工具 |

Linux 單板電腦可作 gateway／Linux 練習平台；與微控制器的架構和週邊不同，不能直接套用另一種晶片的寄存器範例。Mac 是 host，目標板是 target；cross compiler 的輸出 ISA、ABI、作業系統都必須和 target 相符。

<a id="s2"></a>

## 2. CPU、記憶體映射與開機

CPU 執行指令；bus 連到 RAM、flash 與 peripherals。Memory-mapped I/O 把週邊控制映射成位址，但讀寫可能有副作用，例如 read-to-clear 或 write-one-to-clear。先讀 reference manual，不能對所有 status register 使用 read-modify-write。[D2]

**例 E2：位元欄位。** 普通可讀寫 32-bit config register 的 bits 6:4 要設為 5，其他位保留：

```c
/* Concept only: reg is an ordinary local value, not a real address. */
#include <stdint.h>
uint32_t configure(uint32_t reg) {
    const uint32_t mask = UINT32_C(7) << 4;
    return (reg & ~mask) | (UINT32_C(5) << 4);
}
```

輸入 `0xFFFF` 得 `0xFFDF`。若真實寄存器包含 W1C flags，以上方式可能誤清除事件；需使用硬體指定的 set/clear registers 或專用寫入序列。`volatile` 可表達特定存取不可被一般最佳化略去，但不提供互斥、atomicity 或跨核心記憶體排序。

一般 bare-metal 開機可包含：設定 stack、初始化 `.data`／`.bss`、clock／pin mux、進入 main。Linux 系統還有 bootloader、kernel 與 root filesystem。實際 reset sequence 依晶片而定，不能將一塊板的 startup 檔原封不動搬到另一塊。

**例 E3：RAM 預算。** 32 KiB RAM，global/static 8 KiB、三個 task stacks 各 2 KiB、buffers 6 KiB、預留 4 KiB，剩下 8 KiB。這是配置估計；stack watermark、最深呼叫路徑與 interrupt nesting 還需測試。Heap 可用空間不等於任何時候都能成功配置相同大小的連續區塊。

<a id="s3"></a>

## 3. GPIO、UART、SPI、I²C 與 timer

> [!NOTE]
> **讀這一節前：** UART 是雙方事先約定速度的串列傳輸；SPI 由時脈協調資料；I²C 以共用線路與位址選裝置。Baud 指符號率，8N1 是 8 個資料位、無 parity、1 個 stop bit；另有 start bit。Open-drain 只能主動拉低，拉高靠 pull-up。

GPIO input 必須有明確電位；floating input 不能當作可靠 0。Output 的電壓和電流能力取決於器件，motor 或 relay 不能直接接 GPIO 當功率驅動。

| 介面 | 核心概念 | 常見錯誤 |
| --- | --- | --- |
| UART | 非同步串列、兩端約定 baud／frame | 忘了 start/stop bits 與 TX/RX 交叉 |
| SPI | clock、chip select、移位資料 | CPOL/CPHA 不符；選取時間不合規 |
| I²C | SDA/SCL、address、ACK、open-drain | 沒 pull-up；把 7-bit address 與含 R/W 的 byte 混淆 |
| Timer | counter、prescaler、compare/capture | 忽略 ARR+1 或 timer clock 倍頻規則 |

I²C 參考 NXP UM10204；不同速度模式的電氣條件不同。SPI 沒有一份涵蓋所有器件細節的通用 register protocol，command 格式仍看裝置 datasheet。[D3]

**例 E4：UART 與 buffer。** 115200 baud、8N1，每 byte 需 10 bits，因此理想最多 11520 bytes/s。一次 40-byte packet 佔線約 3.472 ms。如果 CPU 最長 20 ms 不消費資料，連續串流可能累積約 231 bytes，256-byte buffer 只有少量餘裕；還需考慮 packet burst 與實際 queue 可用容量。[D4]

**例 E5：timer。** 假設 timer input=48 MHz，prescaler register=47，則 tick=1 MHz；up-counter 從 0 到 ARR=999，一週期 1000 ticks，更新率=1 kHz。公式為 `f_update=f_timer/((PSC+1)(ARR+1))`，僅適用此題指定模式，不直接套用到 center-aligned PWM。

<a id="s4"></a>

## 4. Polling、中斷與 DMA

Polling 不斷查狀態，容易理解但可能空耗 CPU。Interrupt 在事件發生時轉到 ISR；DMA 讓硬體搬運資料，但仍需處理 ownership、completion、cache coherency 與錯誤。DMA 不等於完全沒有 CPU 成本。[D2]

建議 ISR 只做必要的狀態保存、依手冊清 flag、通知 worker；避免無界迴圈、阻塞 I/O、一般 mutex 或大量格式化列印。使用 RTOS 時，只能呼叫文件允許的 ISR API，並遵守 interrupt priority 限制。

```mermaid
flowchart TD
  A[週邊事件] --> B[ISR 記錄狀態]
  B --> C[有界 queue]
  C --> D[Worker 處理]
  D --> E[結果與診斷]
  C --> F[滿載策略]
  F --> E
```

**例 E6：burst 不是平均流量。** 每 1 ms 收一筆，consumer 停 30 ms，至少需容納 30 筆，端點同時事件可能多一筆；若 consumer 回來後也只有 1000 筆/s，它不能清除 backlog。要讓 backlog 下降，恢復時的服務率須高於到達率，或允許丟棄／降低流量。

<a id="s5"></a>

## 5. 由 FSM 建立可理解的故障行為

> [!NOTE]
> **讀這一節前：** 故障設計先列出「可偵測的異常」與「安全反應」。Timeout 是等候超時；watchdog 是系統失去預期進展時的恢復機制；兩者都不能代替需求分析。

把系統狀態與感測值分開。例如 NORMAL、ALARM、SENSOR_FAULT。先決定 fault 優先順序、警報是否 latch、何時允許 reset，才能寫轉移表。熱控制可用 hysteresis：到 30°C 開風扇、低於 28°C 才關，避免雜訊造成頻繁切換；這些是教學數值。

**公開教材原例導讀。** Valvano/Yerraballi Chapter 10、Table 10.2 是兩道路的四狀態 traffic-light controller。觀察 state 如何同時決定輸出、等待時間與依輸入選擇的下一狀態。本文不複製其程式；自學延伸是把 blocking delay 改成 timer event，並測試「兩個方向不可同時綠燈」的不變量。[D5]

Watchdog 只在有意義的健康條件滿足時餵食。若獨立 thread 不管主工作是否卡死都餵狗，watchdog 失去作用。Reset 後保存 reset cause，並確認 actuator 初始狀態；watchdog 也不能替代功能與時序正確性。

<a id="s6"></a>

## 6. Bring-up、Mac 練習與檢核

先做 host model，再做板級 bring-up。第一次接板依序看供電、reset、clock、最小輸出、單一週邊、整合；保留可重現的已知良好版本。Simulator 能證明模型中的轉移，不能量測真實電壓、EMI 或 IRQ latency。

推薦搭配 [P1 虛擬感測器與韌體核心](Projects.md#p1)。將 sensor read 抽成介面，以 CSV 注入值、時間戳、timeout、超量程。程式不要使用真實 GPIO 地址，Mac 才能安全執行。

### 練習

1. 9600 baud、8N1，50 bytes 最少佔線多久？
2. 16 MHz timer，PSC=15，要 2 kHz 更新，ARR 為何？
3. 為何 `volatile int count; count++;` 仍可能有 race？
4. 每次取樣後相對 sleep 100 ms，而計算花 7 ms，長期取樣週期多少？如何改？

<details><summary>解答</summary>

1. `50×10/9600=52.083 ms`，不含間隔。
2. Tick=1 MHz；需 500 ticks，ARR=499。
3. 遞增含讀、加、寫；另一執行者可能在中間插入。需適合環境的 atomic／critical section／mutex。
4. 約 107 ms；以 absolute next-release time 排程，並明訂超時策略。一般 OS 仍有 jitter。

</details>

### 來源

| ID | 來源 | 用途／閱讀位置 |
| --- | --- | --- |
| D1 | [Lee & Seshia 公開教材](https://ptolemy.berkeley.edu/books/leeseshia/) | Cyber-physical modeling；進一步閱讀，不聲稱抄錄完整教材 |
| D2 | [UT Austin Embedded Systems 電子書](https://users.ece.utexas.edu/~valvano/Volume1/E-Book/) | Chapters 6、7、12；平台特定範例須對照手冊 |
| D3 | [NXP UM10204](https://www.nxp.com/docs/en/user-guide/UM10204.pdf) | I²C 電氣與傳輸規範 |
| D4 | [UT Chapter 11](https://users.ece.utexas.edu/~valvano/Volume1/E-Book/C11_SerialInterface.htm) | UART frame 與串列介面 |
| D5 | [UT Chapter 10](https://users.ece.utexas.edu/~valvano/Volume1/E-Book/C10_FiniteStateMachines.htm) | Table 10.2 公開教材原例 |

數值例題為自編；計算已由 `examples/check_models.py` 交叉驗證。完整硬體專案仍為 planned。
