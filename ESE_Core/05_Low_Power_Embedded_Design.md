# Low Power Embedded Design｜低功耗、供電與實體設計

## 入門導讀｜能源是整個系統的預算

先讀 [基礎電學與單位](../Foundations.md)。功率是消耗的速率，能量是累計消耗；電池壽命取決於整個使用週期，不只工作時的峰值。

| 名詞 | 意義 | 直覺例子 |
| --- | --- | --- |
| Duty cycle 工作占空比 | 觀察時間中某種活動占的比例 | 每秒工作 10 ms 是 1% |
| Active / sleep | 工作／低活動模式 | sleep 中哪些模組仍運作要查手冊 |
| Wake-up 喚醒 | 從低功耗狀態恢復工作的過程 | 包含時間與能量成本 |
| Leakage 漏電 | 即使不切換仍可能存在的電流 | 睡眠不等於零電流 |
| Dynamic power 動態功率 | 與電路切換活動相關的功率 | 時脈與電壓會影響 |
| Regulator 穩壓器 | 把供電轉成需要的電壓 | LDO 與 switching converter |
| Quiescent current 靜態電流 | 穩壓器自身運作消耗的電流 | 輕載時可能不可忽略 |
| Transient 暫態 | 狀態改變時的短暫動態過程 | 無線發射瞬間拉大電流 |
| Decoupling 去耦 | 用就近電容等方式支援瞬時電流、降低供電擾動 | 不是容量越大就包辦所有頻率 |
| ESR | 電容的等效串聯電阻 | 瞬時電流也會造成額外壓降 |
| Brownout 欠壓 | 電壓低到無法保證正常工作 | 可能觸發重置 |

### 逐步例子：不能只平均兩個電流數字

每秒工作 10 ms、電流 20 mA，其餘 990 ms 睡眠、電流 0.02 mA。以時間比例加權：20×0.01 + 0.02×0.99 = 0.2198 mA。不是 (20+0.02)/2。若假設可用容量 220 mAh，理想時間約 1001 h；這尚未計入溫度、電池特性、轉換損失與自放電。

> [!NOTE]
> mAh 是電荷量，不是能量。不同電壓電池不能只比較 mAh；能量估算常用 Wh，仍要考慮放電電壓變化與負載條件。

### 系統性看耗電

| 部位 | 可以問的問題 | 代價 |
| --- | --- | --- |
| CPU | 能否少做運算、降低活動或提早完成再睡？ | 速度與喚醒成本 |
| 感測器 | 是否需要一直供電與取樣？ | 穩定時間與漏掉事件 |
| 通訊 | 能否合併資料傳送？ | 等待延遲與 buffer |
| 供電 | 轉換損失與自身耗電多少？ | 成本、雜訊、設計複雜度 |
| 電路板 | 是否有上拉、LED 或漏電路徑持續耗電？ | 可觀察性與功能需求 |

> [!TIP]
> 在時間軸標出「喚醒、取樣、運算、傳送、睡眠」，再對每段的電流乘時間。先做這張表，比先挑最低功耗晶片更容易看出主要消耗。

**暖身與答案：** 睡眠省下 1 mW，但進出睡眠多花 2 mJ，至少睡多久才抵銷成本？2 s。此簡化模型假設額外成本固定，且不犧牲必要功能。

> [!NOTE]
> 本篇按領域概念組織，從基礎走向進階；課程代碼不代表先備要求。原有來源與例題保留供第二輪深入閱讀。

[學習總覽](README.md) · [共通基礎](../Foundations.md)

## 目錄

1. [Power與energy](#s1)　2. [Sleep與duty cycle](#s2)　3. [電池與供電](#s3)　4. [RF與PCB](#s4)　5. [量測與取捨](#s5)　6. [練習與來源](#s6)

<a id="s1"></a>

## 1. 功率低，不一定總能量低

功率P=VI，能量E=∫Pdt。常電壓下可先算charge Q=∫Idt；1mAh=3.6C。mAh不是能量，跨電壓比較電池應用Wh或J。平均電流必須量在同一側供電domain；電源轉換前後不能只比較mA。[L1]

**例 L1：平均電流。** 每秒互斥的四階段：sense 5mA×10ms、compute 8mA×5ms、radio 15mA×4ms、sleep 0.01mA×981ms。總charge=0.15981mA·s，平均0.15981mA=159.81µA。若3V constant，平均功率0.47943mW。若radio和CPU同時工作，應建立重疊狀態或分rail積分，不能重複計算時間。

**例 L2：同工作量不同速度。** A用10mW跑10ms，B用6mW跑20ms；A耗0.1mJ、B耗0.12mJ。B瞬間功率低，總energy卻高。這個比較還沒算等待期間與切換成本。

CMOS切換功率常用`P_dynamic≈α C_eff V² f`理解趨勢；α定義須一致，總功率還含leakage與其他元件。降frequency可降低動態功率，但延長工作時間；若電壓沒降、leakage主導，就不一定節能。

<a id="s2"></a>

## 2. Sleep mode是一份功能契約

選mode前問：RAM是否保留？哪個timer會跑？什麼能喚醒？oscillator啟動多久？GPIO是否保留？最低電流那一行不一定符合應用所需功能。[L1]

**例 L3：break-even。** 深睡比淺睡多花20µJ轉換成本，但等待功率由1mW降至0.1mW，省0.9mW。忽略其他差異時break-even=20µJ/0.9mW≈22.22ms。只睡5ms反而不划算；另需滿足wake-up latency。

**例 L4：batching。** 每次radio喚醒固定耗0.3mJ，每筆資料增0.02mJ；100筆逐筆傳需32mJ，10筆一包、10次傳送需5mJ。代價是較長等待、更大buffer，以及一包遺失的影響。若alarm有20ms deadline就不能無限制batch。

Low-power firmware常用interrupt、DMA、clock gating、按需供電與減少radio喚醒。降低logging也可能有幫助，但先量測，不能以「少一行程式碼」推斷少多少µJ。

<a id="s3"></a>

## 3. 電池、regulator與transient

> [!NOTE]
> **讀這一節前：** LDO 是線性穩壓器，以輸入輸出壓差產生耗散；switching converter 透過開關與儲能元件轉換。Dropout 是維持調節所需的最小壓差，不能把 LDO 當作任意低輸入都能保持輸出。

**例 L5：粗估續航。** 1000mAh，假設有效可用70%，使用L1電池側平均0.15981mA，估計700/0.15981≈4380.20h≈182.51天。這不是保證：溫度、self-discharge、老化、內阻、cutoff voltage與conversion efficiency都可能改變結果。若L1是load側而非battery側，須先換算。

| 元件／特性 | 設計問題 |
| --- | --- |
| LDO | Dropout、quiescent current、熱耗散 |
| Buck | 效率隨負載變化，light-load模式、EMI |
| Battery | 峰值電流、內阻、放電曲線、保護 |
| Capacitor | 有效容量、ESR、偏壓／溫度與漏電 |
| Load switch | Off leakage、inrush、反向電流 |

**例 L6：LDO。** 5V轉3.3V、load100mA，忽略Iq，輸出0.33W、耗散0.17W，效率約66%。若指定熱阻θJA=60°C/W且適用該板與條件，估計junction比ambient高10.2°C。θJA不是不受PCB影響的普遍常數。[L2]

**例 L7：pulse droop。** 電容獨自提供額外20mA、持續2ms，容許電壓下降0.1V，理想C≥IΔt/ΔV=400µF；若ESR=0.5Ω，另有10mV瞬間drop。真實電池也可能提供部分電流，此題是保守的獨立電容模型；還要檢查有效容量與regulator穩定性。

選電源不是只挑低Iq。Radio burst掉壓造成reset，可能讓裝置不斷重啟、耗更多能量。先驗證供電dynamic response，再優化sleep。

<a id="s4"></a>

## 4. RF、PCB與可靠性

> [!NOTE]
> **讀這一節前：** RF 指射頻；PCB 是印刷電路板；return path 是電流回到來源的路徑；EMI 是電磁干擾。訊號線不是獨立的抽象連線，布局、回流與供電都會影響行為。

ECEN5833公開Fall2026課程頁包含power supply、radio、antenna、PCB製作與bring-up；本筆記保留這些方向，不把課程縮成一個電池計算器。[L3]

| 議題 | 原理與設計檢查 |
| --- | --- |
| Decoupling | 縮短高頻電流迴路；位置、return path與封裝寄生皆重要 |
| Return path | 連續參考平面避免高速訊號回流繞路 |
| Antenna | Keep-out、匹配與地平面依reference design，不能任意縮放 |
| Analog/RF干擾 | 開關節點遠離敏感輸入；不要只以「分地」口號處理 |
| Component derating | 額定值不是長期工作點；看溫度與可靠性需求 |
| Bring-up | 先限流供電、查rails、reset、clock，再逐個子系統 |

**例 L8：link budget概念。** 假設TX=0dBm、兩端antenna gain各0dBi、path loss70dB、其他loss3dB，RX≈−73dBm。若receiver sensitivity為−90dBm，算術margin=17dB。這不是保證距離：fading、干擾、方向、人體遮蔽與法規皆另有影響。

Mac可用KiCad整理schematic與PCB學習練習，但它不自動替代課堂指定Altium workflow；正式課程軟體依當期要求。先在Mac做power model與schematic review，再考慮製板。[L4]

<a id="s5"></a>

## 5. 如何得到可信的功耗證據

量測需同時涵蓋µA sleep與mA burst，足夠bandwidth與sample rate，避免量測設備burden voltage改變被測物。平均萬用表讀值可能漏掉短pulse。能量表需記錄rail、voltage、firmware版本、radio條件、取樣窗與儀器。

**公開應用文件導讀。** TI SSZTA01以thermostat說明按功能活動時間拆解能耗。本文L1換用獨立自訂數據，讀者應先畫狀態時間線再積分，不把datasheet典型active current當成整天平均。[L1]

敏感度分析：將radio重傳率、sleep current、採樣間隔改變±20%，比較何者最影響energy。不確定輸入應呈現區間，不畫一條看似精準的多年續航線。

<a id="s6"></a>

## 6. 練習

1. 2mA工作10ms、2µA睡990ms，一秒平均多少？
2. 兩顆相同1000mAh電池串聯，是否等於2000mAh？
3. 相同α、C與f下，V由1.2降為1.0，動態功率比？
4. 只降低sampling rate可能犧牲什麼？

<details><summary>解答</summary>

1. 0.02+0.00198=0.02198mA=21.98µA。
2. 理想串聯電壓相加、Ah容量不加；能量增加。實際受不匹配與保護限制。
3. `(1/1.2)²≈0.6944`，只比較dynamic component且假設仍能運作。
4. 偵測延遲、可觀測頻寬與事件漏失；需回到系統規格。

</details>

| ID | 來源 | 查核重點 |
| --- | --- | --- |
| L1 | [TI SSZTA01](https://www.ti.com/document-viewer/lit/html/SSZTA01/GUID-71673865-16A3-48B6-91B4-4725395D3856) | Energy、duty cycle、power modes |
| L2 | [TI SLVA462](https://www.ti.com/lit/an/slva462/slva462.pdf) | Thermal resistance與耗散估計 |
| L3 | [ECEN5833 Fall2026](https://sites.google.com/colorado.edu/ecen-5833/home) | 供電、RF、PCB與bring-up課程範圍 |
| L4 | [KiCad macOS官方下載](https://www.kicad.org/download/macos/) | Mac自學EDA工具支持 |

L1–L8為教科書型自編例題，P5尚為planned；沒有實測電池續航或完成PCB認證。
