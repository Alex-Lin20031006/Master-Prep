# Mac-first Embedded Projects｜學習專案規劃

> 所有完整專案狀態：**planned**。以下是規格與里程碑，不是已完成的作品。估時是針對自學的工作量預估，不含安裝疑難與正式課堂作業；每週6–8小時可分階段完成。查核：2026-09-29。

[課程筆記總覽](README.md)

## 建議先選哪個

先完成P1，再選P2加深即時理論；接著以P4串接IoT形成一個有測試證據的作品。P5／P6各選一個小實驗並行；P7適合logic學完後，P8留到Linux基礎熟悉再做。不需要同時完成八個專案。

| 專案 | 環境 | 估時 | 對應課程 |
| --- | --- | --- | --- |
| [P1 虛擬感測器與可測試韌體核心](#p1) | Mac 原生 | 18-28 小時 | 5613 + 5813 |
| [P2 RM／EDF 排程分析與視覺化工具](#p2) | Mac 原生 | 16-24 小時 | 5623 |
| [P3 Linux 感測資料收集服務](#p3) | Mac + Linux VM | 24-36 小時 | 5813 + 5713 |
| [P4 可斷線復原的本機 IoT 管線](#p4) | Mac 原生 | 20-32 小時 | 5823 + 5773 |
| [P5 低功耗節點能量預算工具](#p5) | Mac 原生 | 12-20 小時 | 5833 + 5823 |
| [P6 感測雜訊與馬達 PI 控制模擬器](#p6) | Mac 原生 | 18-30 小時 | 5853 + 5623 |
| [P7 RTL 串流處理與 FIFO 驗證](#p7) | Mac 原生 simulation | 24-40 小時 | 5863 |
| [P8 可重建的 Embedded Linux 映像](#p8) | Linux build host + QEMU | 30-50 小時 | 5713 + 5613 |

<a id="p1"></a>
## P1 — 虛擬感測器與可測試韌體核心

**狀態：planned｜Mac 原生｜入門｜18-28 小時**

### 目標

用同一份 C 核心處理合成感測資料，建立採樣、ring buffer、hysteresis、fault 與 logging。這是日後火災偵測專案的軟體基礎。

### 工具與環境

C11 compiler、Python 3、Git；可選 AddressSanitizer。第一版不需要開發板、Docker 或雲端。

### 架構

CSV replay adapter → sample validator → fixed-size queue → state machine → event CSV；所有硬體讀取留在 adapter。

### 輸入／輸出契約

CSV 欄位 t_ms、seq、temperature_c、valid；固定 100 ms 理想取樣。輸出 t_ms、state、reason、dropped_count。溫度門檻是教學設定，不是火警標準。

### 里程碑

1. M1：先寫輸入 schema 與 NORMAL／ALARM／SENSOR_FAULT 轉移表；手算六個小情境。
2. M2：完成 C decode、queue、溫度門檻與 reset policy；使用本次提供的 firmware_core.c 作小型參考。
3. M3：加入 CSV replay 與錯誤注入；以同一輸入比對預期事件。
4. M4：整理 CLI、測試命令、架構圖與 2 分鐘 demo。

### 驗收標準

至少 12 個命名案例：正常、等於門檻、上下抖動、timeout、無效值、滿 queue、reset 等；每個案例 exact-match 預期事件。編譯無警告，支援的 sanitizer 下無錯誤。

### GitHub交付

src/、tests/fixtures/、docs/spec.md、test-results.txt、sample-output.csv。README 區分 host-tested 與 planned hardware adapter。

### 可選硬體擴展

可選：把 CSV adapter 換成 Raspberry Pi 3B 的數位感測器讀取。先確認 3.3V 介面；類比感測器另需 ADC。核心 state machine 不改。

### 能力界線

Host 模型不能證明感測器準確度、警報可靠度或 MCU interrupt timing；不作實際生命安全警報裝置。

### 對應閱讀

C core 筆記、Clang ASan、UT Austin FSM。


<a id="p2"></a>
## P2 — RM／EDF 排程分析與視覺化工具

**狀態：planned｜Mac 原生｜入門至中階｜16-24 小時**

### 目標

把公式變成能重現 deadline miss 的工具，比較 utilization bound、response-time analysis 與模擬結果。

### 工具與環境

Python 3；先用標準函式庫與 CSV，圖表再加入 matplotlib。

### 架構

Task JSON → model validator → RM／EDF engine → timeline／deadline checker → CSV 與圖。

### 輸入／輸出契約

每 task：id、C、T、D、offset；第一版限定整數 ticks、單核、零 context-switch cost、D=T、無 blocking。規則不符時拒絕或明確警告。

### 里程碑

1. M1：完成 C/T/D 與模型檢查；手畫兩 task 的 0-20 ticks。
2. M2：實作 ready queue、preemption、tie-breaker、deadline check。完成邊界先檢查再釋出同時間新 job 的一致順序。
3. M3：加入 RM bound 與 B=J=0 的 RTA，對照筆記案例。
4. M4：輸出 timeline、response times、miss count；加入一個故意過載案例。

### 驗收標準

(1,4),(1,5),(2,10) 得 R=[1,2,4]；harmonic (1,2),(2,4) 在 U=1 仍可排。過載 (3,4),(3,5) 能報 miss。模擬 horizon 與未完成 jobs 必須顯示。

### GitHub交付

至少 6 組 tasksets、獨立手算答案、兩張 RM/EDF 對照圖與測試。圖軸標示 simulated time。

### 可選硬體擴展

可選：到 Linux VM／實體 RTOS 記錄 task timestamps，再比較 observed jitter；另列實機模型，不能混入理想模擬報告。

### 能力界線

有限 horizon 沒有 miss 不等於任意 task model 的全時間證明；macOS／VM wall-time 不是 hard real-time 保證。

### 對應閱讀

Liu-Layland 原論文、York RTA、Zephyr native_sim。


<a id="p3"></a>
## P3 — Linux 感測資料收集服務

**狀態：planned｜Mac + Linux VM｜中階｜24-36 小時**

### 目標

把 P1 資料串流變成有 framing、bounded queue、持久化與優雅關閉的 Linux service，練習 POSIX 與 concurrent programming。

### 工具與環境

M2 上 Linux ARM64 VM 作 user-space 自學；C compiler、pthread、socket、SQLite 或 append-only log。Linux-specific 部分在 VM 執行。

### 架構

Producer client → TCP listener → framed decoder → bounded work queue → writer thread → database；signal handler只通知退出。

### 輸入／輸出契約

固定長度 header 含 version、payload_len、seq，payload 上限例如 256 bytes；先定義 wire byte order。輸出接受／拒絕／重複／持久化計數。

### 里程碑

1. M1：先單執行緒完成 short read/write 與 framing，拒絕 oversized payload。
2. M2：分離 receiver/writer；condition-variable wait以predicate迴圈處理。
3. M3：加入 disconnect、慢client、queue full、disk error注入與退出流程。
4. M4：在 Linux VM 記錄版本、測試命令與固定負載下的 latency。

### 驗收標準

分割成 1-byte chunks 仍能還原 1000 筆 records；重複 seq 有既定策略；malformed length 不造成無界配置；SIGTERM 後依規格 drain 或記錄丟棄。

### GitHub交付

Protocol spec、至少 8 個 integration cases、thread ownership 圖、latency 分布與環境註記。

### 可選硬體擴展

可選：同服務移到 Pi 3B，以 SSH 管理。再加 Linux service manager；driver 練習留到 disposable VM。

### 能力界線

正式 ECEN5713 Spring2026 公開環境仍指定 x86-64；ARM64 VM是自學路線。不得宣稱已符合當期課堂映像／工具鏈。

### 對應閱讀

OSTEP、Linux kernel docs、UTM、ECEN5713。


<a id="p4"></a>
## P4 — 可斷線復原的本機 IoT 管線

**狀態：planned｜Mac 原生｜中階｜20-32 小時**

### 目標

用虛擬裝置、MQTT broker 與儲存端，展示重送、去重、過期資料與離線 buffering，比只有 dashboard 更有工程價值。

### 工具與環境

Python 3、Eclipse Mosquitto、SQLite；CLI先行，dashboard為選配。先用localhost，無需付費雲端帳號。

### 架構

Virtual nodes → bounded outbox → local broker → idempotent consumer → SQLite → report。BLE GATT adapter後續才做。

### 輸入／輸出契約

Schema包括 device_id、boot_id、seq、sample_time、value、unit、quality、schema_version；DB用三欄key去重。

### 里程碑

1. M1：一個publisher與subscriber正常傳10筆，schema validation完整。
2. M2：加入bounded outbox、retry/backoff與restart recovery。
3. M3：停止broker 60秒後重啟；注入重複、out-of-order、過期sample。
4. M4：輸出接受／重複／過期／丟棄報表，另做權限與TLS的測試配置。

### 驗收標準

同key重播不增加DB record；不同boot_id的seq=0可接受；queue滿時依規格drop或block且記錄。設定capacity至少涵蓋測試期間輸入，才能主張該測試無資料遺失。

### GitHub交付

消息schema、broker設定（無秘密）、fault-injection腳本、DB驗證查詢、failure/recovery時間線。

### 可選硬體擴展

可選：Pi 3B做gateway，再加入BLE sensor。先mock characteristic bytes；實際radio參數與throughput另外量測。

### 能力界線

MQTT QoS2不等於資料庫與actuator業務恰一次；虛擬node不是已連實體的digital twin。

### 對應閱讀

OASIS MQTT5、Bluetooth SIG Primer、Mosquitto。


<a id="p5"></a>
## P5 — 低功耗節點能量預算工具

**狀態：planned｜Mac 原生｜入門至中階｜12-20 小時**

### 目標

把 active/sleep/radio 狀態轉為可追查的能量與續航估計，學會不確定性、battery-side／load-side與wake-up成本。

### 工具與環境

Python 3、CSV／JSON；可選 matplotlib、KiCad schematic。第一版完全不用電池或量測儀器。

### 架構

State profile + voltage/efficiency assumptions → charge/energy integration → parameter sweep → sensitivity report。

### 輸入／輸出契約

每狀態 duration_ms、current_mA、rail_voltage；互斥週期需驗證總時間。電池容量、derating、Iq、efficiency作獨立假設。

### 里程碑

1. M1：用筆記L1手算並實作常電壓模型。
2. M2：加入多rail與converter換算，明確標示電流在哪一側。
3. M3：比較batching、sample period與sleep break-even。
4. M4：對radio current與sleep leakage掃描範圍，出具低／中／高估計。

### 驗收標準

L1平均159.81µA；1000mAh×70%模型約182.51天。輸入負時間、效率>1、零容量等須拒絕；圖表不能標成實測續航。

### GitHub交付

Assumptions.md、資料來源欄、單位檢查、sensitivity圖、兩方案比較與反例「功率低但能量高」。

### 可選硬體擴展

可選：MCU開發板與足夠bandwidth的current measurement equipment。量測waveform後匯入模型，解釋誤差；Pi3B不作超低功耗MCU替身。

### 能力界線

忽略self-discharge／temperature的多年估計不可靠。KiCad示意不是已通過DFM、EMI或電池安全驗證的PCB。

### 對應閱讀

TI SSZTA01、TI thermal note、KiCad。


<a id="p6"></a>
## P6 — 感測雜訊與馬達 PI 控制模擬器

**狀態：planned｜Mac 原生｜中階｜18-30 小時**

### 目標

結合校正、量化、filter、encoder與plant model，觀察latency、saturation與anti-windup如何影響速度控制。

### 工具與環境

Python 3、NumPy／SciPy／matplotlib；最初可用標準函式庫完成簡化Euler模型。無需MATLAB授權或motor。

### 架構

Setpoint → discrete PI → saturated driver model → DC motor differential equations → noisy sensor/encoder → filter → feedback。

### 輸入／輸出契約

固定seed、dt、motor parameters、supply limit、load torque、Kp/Ki；輸出time、omega、current、u、error、integral與quality。

### 里程碑

1. M1：先跑open-loop，對照解析steady-state 0.0999001rad/s的公開模型。
2. M2：加入quantization、noise、encoder window與校正。
3. M3：加入PI，分開測無／有anti-windup、load step與sensor timeout。
4. M4：dt減半做收斂比較，記錄overshoot、settling time、steady error與飽和時間。

### 驗收標準

零負載open-loop長時間結果與解析值相符（先訂例如1%容差）；dt減半結果收斂；故意大setpoint可展示windup差異。性能目標先設計後量測，不預填「已達成」。

### GitHub交付

Model assumptions、parameter units、seed、CSV、至少四張response比較圖、三個failure cases。

### 可選硬體擴展

可選：低電壓motor、driver、encoder、獨立限流電源、MCU與保護。先確認stall current、mechanical limits，GPIO只作控制。

### 能力界線

線性模型省略非線性與真實driver；穩定的simulation不是硬體穩定性保證。這也不是EV inverter或高電壓實作。

### 對應閱讀

Michigan CTMS、Analog Devices MT-001、UT ADC。


<a id="p7"></a>
## P7 — RTL 串流處理與 FIFO 驗證

**狀態：planned｜Mac 原生 simulation｜中階至進階｜24-40 小時**

### 目標

用可重現testbench驗證saturating adder、ready/valid與FIFO，學會waveform與cycle-level正確性。

### 工具與環境

SystemVerilog、Verilator、C++或支援的SV testbench；Python golden model。先選一套測試架構並固定版本。

### 架構

Source driver → ready/valid stage → saturating adder → synchronous FIFO → sink scoreboard。

### 輸入／輸出契約

8-bit operands、valid、ready、reset；output有8-bit saturated sum。FIFO depth先固定16，明訂同時push/pop與reset丟棄。

### 里程碑

1. M1：純組合adder，全部65536對輸入與golden比較。
2. M2：加pipeline valid，逐cycle比較預期latency。
3. M3：加FIFO與random backpressure，assert stall時資料穩定。
4. M4：注入reset、full／empty邊界；保存seed、waveform與最小failure trace。

### 驗收標準

65536組adder結果通過；至少10000個已接受transaction順序一致、無重複／遺失。計數只在ready&&valid時增加；reset後預期佇列同步清除。

### GitHub交付

rtl/、tb/、golden/、工具版本、測試summary、關鍵波形與介面規格。

### 可選硬體擴展

可選：確認校方支援FPGA與工具後做synthesis／STA／board test；先借板。Mac simulator成功不表示能原生產生任意FPGA bitstream。

### 能力界線

同步FIFO不當作async FIFO。RTL模擬不能驗證analog metastability、pin voltage或board timing。

### 對應閱讀

AMD UG901／UG949、Verilator、Logic Design筆記。


<a id="p8"></a>
## P8 — 可重建的 Embedded Linux 映像

**狀態：planned｜Linux build host + QEMU｜進階，選做｜30-50 小時**

### 目標

將P3服務加入最小Linux映像，保存建置配置與啟動證據；學會toolchain、kernel、rootfs、package與系統更新責任。

### 工具與環境

Linux build host、Buildroot、QEMU；優先遵循target官方defconfig。M2可先評估Linux VM，x86-64-only流程則用可用的遠端x86-64 host。

### 架構

Versioned config + source hashes → build host → toolchain/kernel/rootfs → QEMU guest → P3 service → host integration tests。

### 輸入／輸出契約

Pinned Buildroot release、defconfig、external tree、package recipe、rootfs overlay；output為映像、manifest、boot log與test results。

### 里程碑

1. M1：未改動的受支援QEMU target啟動到shell，保存完整命令。
2. M2：用BR2_EXTERNAL整理自訂package與設定，不手改生成target目錄作唯一來源。
3. M3：加入P3服務與啟動配置，從host測試網路與持久化策略。
4. M4：乾淨build directory重建並重跑功能測試；檢查licenses與source provenance。

### 驗收標準

乾淨重建可開機且通過同一組P3 smoke tests；有版本與checksum manifest。若未控制所有timestamps等因素，只主張功能可重建，不主張bit-for-bit reproducible。

### GitHub交付

defconfig、external-tree/、build notes、boot log、manifest、failure recovery design。不要把大型build cache推上GitHub。

### 可選硬體擴展

可選：換成Pi3B的明確supported configuration，另外驗證boot與peripherals；A/B更新先做檔案模型再做實機。

### 能力界線

耗時與disk使用取決於config；不預設你的RAM足夠。不更換Mac也可用校方／遠端host，但資源可用性與費用需開始前確認。

### 對應閱讀

Buildroot manual、QEMU Arm docs、ECEN5713。

## 12週安排範例

這是開始後的相對週次，並非承諾在固定日期前完成。若每週時間不足，延長週期即可。

| 週 | 重點 | 必交證據 |
| --- | --- | --- |
| 1–2 | P1規格、C core、unit tests | fixtures與測試log |
| 3–4 | P1 replay／fault cases，P2手算與模型 | demo＋RTA報告 |
| 5–6 | P4 localhost正常路徑與schema | 訊息與DB查詢 |
| 7–8 | P4斷線／去重／過期資料 | fault recovery時間線 |
| 9 | P5功耗預算 | assumptions＋敏感度圖 |
| 10 | P6 open-loop與校正，或P7 adder | 與獨立模型對照 |
| 11–12 | 選定一個主作品整理與補測 | README、架構、復現命令、已知限制 |

P3/P8可替換上述後半段作Linux主線；不要在短期同時啟動所有主線。

## 硬體採購延後決策

先使用現有MacBook Air M2，P1/P2/P4/P5/P6/P7 MVP不要求新增硬體。需要Linux時評估可用RAM／磁碟再建VM；不預設你的機器有16GB。現有Pi3B優先作P3/P4 gateway，MCU、FPGA、motor與量測儀器等到選定課堂／專案再核對型號與電氣條件，不在此捏造即時價格。

## 完成作品時的README模板

Problem → Requirements → Architecture → Setup（工具版本）→ Run → Tests → Results（環境與單位）→ Limitations → Planned extensions → References。

不要只放一張成功截圖；保留一個故障案例和修復後的證據。之後開始實作時，先報P編號，我們再從環境、最小版本到測試逐步完成。
