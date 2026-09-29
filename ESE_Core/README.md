# ESE Core Study Guide｜核心課程自學筆記

> [!IMPORTANT]
> **閱讀主線改為領域基礎。** 先讀 [共通基礎](../Foundations.md)，再讀每篇「入門導讀」。下方課程對照只作資源索引，不是必須照做的課表；專案是選讀實作，不決定知識範圍。

| 順序 | 先建立的概念 | 筆記 |
| --- | --- | --- |
| 1 | 計算如何連到週邊 | [嵌入式系統設計](01_Embedded_System_Design.md) |
| 2 | 工作、時間與共享資源 | [即時系統](02_Real_Time_Embedded_Systems.md) |
| 3 | 程式、記憶體與 OS | [嵌入式軟體與 Linux](03_Embedded_Software_and_Linux.md) |
| 4 | 通訊層次、交付與信任 | [物聯網](04_IoT_Firmware_and_Industrial_IoT.md) |
| 5 | 電力、能量與系統預算 | [低功耗](05_Low_Power_Embedded_Design.md) |
| 6 | 量測、回授與實體動態 | [感測與馬達](06_Embedding_Sensors_and_Motors.md) |
| 7 | 平行電路與時間約束 | [FPGA](07_Programmable_Logic_Embedded_Design.md) |

每篇先讀詞彙表和小例子，再進原本的計算與設計分析。遇到沒有把握的符號，先回到單位、資料流與時間軸，不必一開始就背公式。



> 查核日期：2026-09-29（Asia/Taipei）。以使用者提供的七門核心課程圖片為範圍。這是繁體中文＋英文術語的入門到中階自學材料，不是官方課堂講義、2027考綱或學分替代。

[Repository README](../README.md) · [Mac 優先專案規劃](Projects.md)

## 課程範圍與合併方式

校方公開ESE頁面目前寫 **任選五門core courses**，不是七門全部必修。另有兩門ESE electives（或更多core）與三門open 5000-level electives，個人選課需按適用catalog及advisor核可。本文仍完整整理圖片中的七門，讓你可預習與選擇。

| 筆記 | 對應課程 | 內容 |
| --- | --- | --- |
| [Embedded System Design](01_Embedded_System_Design.md) | ECEN 5613 | 需求、GPIO、UART／I²C、interrupt、DMA、FSM |
| [Real-Time Embedded Systems](02_Real_Time_Embedded_Systems.md) | ECEN 5623 | 時間模型、RM／EDF、RTA、blocking與驗證 |
| [Embedded Software + Advanced Embedded Linux](03_Embedded_Software_and_Linux.md) | ECEN 5813 + 5713 | C、testing、POSIX、concurrency、Buildroot |
| [IoT Firmware + Industrial IoT](04_IoT_Firmware_and_Industrial_IoT.md) | ECEN 5823 + 5773延伸 | Event-driven、BLE、MQTT、可靠性與工業情境 |
| [Low Power Embedded Design](05_Low_Power_Embedded_Design.md) | ECEN 5833 | Energy、sleep、battery、power、RF／PCB |
| [Embedding Sensors and Motors](06_Embedding_Sensors_and_Motors.md) | ECEN 5853 | Calibration、ADC、filter、encoder、motor、PI |
| [Programmable Logic Embedded Design](07_Programmable_Logic_Embedded_Design.md) | ECEN 5863 | RTL、fixed point、pipeline、FIFO、CDC、STA |

5813與5713有明確基礎／進階關係，因此合成一份。5773作5823的工業延伸，並非宣稱校方將兩課視為固定連續序列。其餘electives不是這次主要範圍；5593可參考既有[Computer Architecture](../Computer_Architecture.md)，本次沒有冒稱已按該課完整重寫。尚未確認的Advanced Programmable Logic實際syllabus不列成已完成筆記。

## 如何讀

1. 先複習[Logic Design](../Logic_Design.md)與[Organization](../Computer_Organization_and_Design.md)的binary、C記憶體、interrupt與cache基本概念。
2. 先讀03的C／testing，再讀01建立完整系統觀。
3. 讀02，學會區分C、T、D、R與blocking，再做P2。
4. 04與05一起看：event-driven、radio、energy互相影響。
5. 06把時間、雜訊與control串起來；07把同樣的資料流改用RTL思考。
6. 03後半Linux在基礎C與Git熟練後進行；P8最後再選。

每章都有原理、明示假設的教科書型自編例題、生活／工程應用、練習與可展開答案。公開教材原例另標來源；沒有虛構付費書題號或官方解答。

## MacBook Air M2 的分層路線

| 層級 | 可先做 | 不能因此主張 |
| --- | --- | --- |
| macOS原生 | C／Python、models、MQTT、RTL simulation | 真實MCU時間或硬體功耗 |
| Linux VM | POSIX／Linux服務、部分build／emulation | x86-64課堂映像必定支持ARM64 |
| 遠端支持環境 | 課堂指定x86-64／FPGA工具 | 已有權限、免費或已完成配置 |
| 選配實體板 | Pi gateway、MCU sensor、FPGA test | Host model已替代板級測試 |

ECEN5713的公開Spring2026頁面仍指定x86-64 host；ECEN5833提到Altium，5853頁面含明顯年代混雜的OS資訊。這些只能作工具風險提示，不能視為2027春季已確認要求。無需現在買另一台電腦；先完成原生Mac專案，之後確認校方remote／lab資源。

## 可重現的例題驗證

從repo根目錄：

```sh
python3 ESE_Core/examples/check_models.py
cc -std=c11 -Wall -Wextra -Werror ESE_Core/examples/firmware_core.c -o /tmp/firmware_core
/tmp/firmware_core
```

本次在工作環境實際執行：RTA的可排／不可排案例、數值例題、65,536組飽和加法reference比較、C解碼／overflow guard／ring buffer的滿空與回繞。這不表示新的RTL已模擬，也沒有做網路服務、Buildroot、RTOS或硬體實驗。完整P1–P8都是 **planned**；檢查腳本是教學小工具。

## 來源與查核方式

- 課程範圍：[CU ESE官方頁](https://www.colorado.edu/ecee/academics/graduate-programs/professional-masters/embedded-systems-engineering-and-internet-things)及[course catalog](https://catalog.colorado.edu/graduate/colleges-schools/engineering-applied-science/programs-study/electrical-computer-and-energy-engineering/)。不把舊學期page當2027開課保證。
- 概念優先用作者公開教材、原論文、標準與官方工具文件；各章有對應來源。公開共享筆記僅在作者與依據可追查時採用，沒有把搜尋摘要當成完整讀過的付費教材。
- 數字由明示模型重算；額定值／實測值／教學假設分開。CTMS站本次全文讀取受限，已在感測筆記清楚註明官方索引可見內容與代數驗算範圍。
- 若要實作，以當時工具版本、目標board手冊與test results為準；所有尚未執行的project功能標為planned。

## 學習成果檢核

- [ ] 用一段話定義需求與可量測驗收條件。
- [ ] 不混淆average latency與deadline guarantee。
- [ ] 能解釋volatile／atomic／mutex、notification／indication、QoS／application dedup。
- [ ] 能列清楚power model的rail、時間與單位。
- [ ] 能用獨立reference檢查sensor model與RTL運算。
- [ ] 每個demo都附已測與未測範圍，不將planned功能寫成履歷成果。

