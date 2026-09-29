# IoT Firmware + Industrial IoT｜物聯網韌體與工業延伸

## 入門導讀｜先理解通訊，再理解物聯網

物聯網把裝置資料送到其他系統，也可能接收命令。它同時包含感測、韌體、網路、服務與維運。能送出一筆資料只是起點；接收者還要知道資料屬於誰、何時量到、有沒有重複或過期。

| 層次 | 要解決的問題 | 名詞 |
| --- | --- | --- |
| 實體與鏈路 | 鄰近設備如何傳送 bits？ | 無線電、Ethernet、BLE |
| 網路 | 資料如何跨網路到目的地？ | IP 位址、router 路由器 |
| 傳輸 | 端點如何交換資料？ | TCP 位元組流、UDP datagram |
| 應用 | 收到的資料代表什麼？ | MQTT、HTTP、資料格式 |
| 信任與管理 | 誰可以連線、更新與下命令？ | 身分驗證、授權、OTA |

BLE 不必經過 IP 才能和手機交換資料；MQTT 常經 TCP，TCP 可靠位元組流也不會自動提供應用訊息邊界。不同層的「封包」與「訊息」不是一律一對一。

| 名詞 | 白話意思 |
| --- | --- |
| Node 節點 | 收集或處理資料的網路裝置 |
| Gateway 閘道器 | 在裝置端與其他網路／協定之間連接或轉換 |
| Broker 訊息代理 | 依 topic 接受並轉送發布的訊息 |
| Publish / subscribe | 發布到主題／訂閱感興趣的主題 |
| Payload | 訊息中真正要交付的資料內容 |
| QoS | 指定協定層級的交付品質規則 |
| Acknowledgment / ACK | 接收方對某一步驟的確認 |
| Idempotent 冪等 | 同一操作重做多次，效果與一次相同 |
| Authentication 身分驗證 | 確認對方是誰 |
| Authorization 授權 | 決定對方能做什麼 |
| Encryption 加密 | 保護內容不被未持鑰者直接讀取 |
| OTA | 經遠端通道更新裝置軟體 |

### 逐步例子：為何會重複開燈？

裝置送「切換燈的狀態」，接收者執行了，回覆卻遺失。裝置重送後燈被切回去。把命令設成「把燈設為 ON」，重送仍是 ON，這是冪等設計。若命令是「發放一份商品」，還需唯一命令 ID 與保存處理結果，不能只靠重送。

> [!IMPORTANT]
> MQTT 的 QoS 是協定流程保證；資料庫更新、馬達動作或金錢交易是否恰好一次，需要應用層設計。加密也不會自動限制合法帳號能做的事。

### 先理解 BLE 的兩組不同角色

Central / peripheral 關係到連線角色；GATT client / server 關係到誰發起資料操作、誰提供資料。Characteristic 是 GATT 中有型別與屬性的資料項目，service 是相關項目的分組。不能把 central 永遠等同 GATT client。

**暖身與答案：** 訊息有裝置 ID、序號和取樣時間，為什麼比只有溫度好？可分辨來源、重複／遺失與資料新舊；但時間仍須考慮時鐘同步誤差。日常應用包括電表、環境監測、物流追蹤，不限某個感測專案。

> [!NOTE]
> 本篇按領域概念組織，從基礎走向進階；課程代碼不代表先備要求。原有來源與例題保留供第二輪深入閱讀。

[學習總覽](README.md) · [共通基礎](../Foundations.md)

## 目錄

1. [系統與事件模型](#s1)　2. [BLE](#s2)　3. [MQTT／gateway](#s3)　4. [安全與可靠性](#s4)　5. [Industrial IoT](#s5)　6. [練習與來源](#s6)

<a id="s1"></a>

## 1. Node、gateway、broker 與 application

Sensor node負責取樣與有限處理；gateway可轉換BLE與IP應用協定；broker分發訊息；application儲存、顯示與決策。不是每個node都需要直接連Internet。ECEN5823官方說明著重低能耗、event-driven firmware與BLE／Thread類wireless protocols；MQTT是本文的應用層延伸，不能替代BLE韌體內容。[I1]

```mermaid
flowchart TD
  N[Sensor node] -->|BLE| G[Gateway]
  G -->|MQTT| B[Broker]
  B --> D[資料儲存]
  B --> V[Dashboard]
  V -->|命令與權限| B
  B --> G
```

Event-driven firmware把事件送給狀態機：BOOT→IDLE→SAMPLING→REPORTING，再回IDLE。每個事件handler應有界，長工作切段或移至worker，否則會阻塞其他事件。應處理timeout、busy、retry與disconnect，而非只寫成功路徑。

**例 I1：狀態逾時。** ADC開始後預期10 ms完成；設定15 ms timeout。若逾時，應取消／標記舊請求並進入錯誤處理；遲到的completion需用request_id辨認，避免當作下一次取樣。15 ms只是題目設定，真實值由datasheet與排程分析決定。

<a id="s2"></a>

## 2. Bluetooth Low Energy：不要混淆角色

> [!NOTE]
> **讀這一節前：** Advertising 是 BLE 裝置廣播可被發現等資訊；connection 是建立後依約定交換資料；MTU 是特定協定層可處理的最大單位。Notification 不要求 GATT 層確認，indication 有相應確認流程；不能把兩者直接當成端到端應用成功。

| 層次 | 問題 | 術語 |
| --- | --- | --- |
| GAP／link | 誰advertise、scan、建立連線？ | Peripheral、central等角色 |
| ATT／GATT | 資料如何被組織與存取？ | Attribute、service、characteristic、descriptor |
| Application | 此值代表什麼？ | 單位、比例、版本、有效旗標 |

GATT server保存attributes，client發起操作；central不必永遠等於client。Notification沒有ATT層confirmation；indication有confirmation，但都不等於「資料已永久寫入資料庫」。不可把notification直接說成完全無線鏈路重傳。[I2]

**例 I2：payload長度。** 對一般ATT Handle Value Notification，ATT_MTU=23時value最大20 bytes（扣opcode1+handle2）；MTU=247時可為244 bytes。這不保證單一link-layer packet或指定throughput；還受data length、PHY、connection interval、event長度與peer限制。

**例 I3：二進位感測值。** 自訂temperature characteristic使用signed16 little-endian，單位0.01°C。25.34°C→2534→0x09E6→bytes E6 09；−5.00°C→−500→16-bit二補數0xFE0C→0C FE。Schema必須同時寫明signedness、byte order、scale與無效值，不只給UUID。

### 2.1 Connection與功耗

廣播間隔越短，通常越容易被發現但radio活動更多；連線參數影響延遲與耗能。不要只看平均資料bytes/s，還需計算connection events、receive windows與重傳。實際可接受參數由雙方stack與規範決定，不能任意設定後假設peer接受。

BLE pairing、bonding、encryption、application authorization是不同層次。連線加密不自動代表所有client都能下控制命令。Mac可先mock GATT資料與狀態機；真實radio測試需合適peer與硬體，列為planned。

<a id="s3"></a>

## 3. MQTT：傳送保證不等於業務保證

MQTT透過broker按topic分發。Payload是application定義的bytes；topic、schema與timestamp都屬系統契約。[I3]

| QoS | 傳輸語義 | 應用注意 |
| --- | --- | --- |
| 0 | At most once | 可能遺失 |
| 1 | At least once | 可能重複，consumer需idempotency |
| 2 | Exactly once 的協定交付流程 | 不保證跨DB／actuator的業務交易恰一次 |

Retained message保存某topic的最近retained值，不是歷史資料庫；新subscriber可能取得舊狀態。Last Will可表示非正常斷線，但偵測與發布不會瞬間發生，需考慮keep-alive與Will Delay等設定。

**例 I4：去重。** 封包使用 `(device_id, boot_id, seq)` 當key。QoS1重送同key時，DB以unique constraint避免多插入；重新開機seq歸0但boot_id不同，仍是新資料。這不是單靠MQTT設定能做到的效果。

建議schema：`schema_version, device_id, boot_id, seq, sample_time, value, unit, quality`。若node無UTC，記錄monotonic ticks與gateway receive time；不要假裝兩者是同一時間。

**例 I5：離線容量。** 每秒1筆，每筆序列化120 bytes，離線24h需10,368,000 bytes≈9.89 MiB（未含index、filesystem、重送metadata）。設定有界outbox、滿載策略與重連限速；無界retry可能耗盡disk。

<a id="s4"></a>

## 4. Reliability、安全與OTA設計

> [!NOTE]
> **讀這一節前：** Retry 是失敗後重試；backoff 是逐步延長重試間隔；deduplication 是識別重複資料。TLS 保護通道，簽章用於驗證來源與完整性；secure boot 驗證啟動鏈，rollback protection 防止退回不允許的舊版本，責任不同。

| 故障 | 需要的機制 | 測試方式 |
| --- | --- | --- |
| Broker停機 | Backoff、bounded queue | 關閉本機broker後復原 |
| 訊息重複 | Idempotent consume | 重播相同seq |
| 舊值 | TTL／timestamp／quality | 注入過期樣本 |
| 憑證錯誤 | 拒絕連線並記錄原因 | 測試憑證、錯hostname |
| 更新斷電 | 驗證、rollback、狀態原子化 | 先用檔案模型注入各階段中斷 |

TLS驗證server身分與傳輸保護，topic ACL限制權限。裝置credential不能直接commit到GitHub。關閉certificate verification不是修好TLS。專案先綁定localhost，設計明確後再擴展網路部署。

**例 I6：backoff。** 自訂base=1s，cap=32s，full jitter範圍`[0,min(32,2^k)]`。k=0..5上界1、2、4、8、16、32s；成功後重設。這是設計選擇，不是MQTT強制規範。固定random seed可做可重現測試。

<a id="s5"></a>

## 5. 工業延伸：資料價值與控制責任

IIoT不只是多裝幾個sensor。需考慮設備壽命、斷網運作、維護窗口、校正、資產識別與安全域。分析用途常可接受秒級延遲；快速閉迴路控制通常應放在本地控制器，不能把一般Internet連線當成有界deadline通道。[I4]

**例 I7：maintenance指標。** 假設motor振動RMS由0.2升到0.6（自訂normalized units），可觸發「需檢查」事件，但不能沒有fault label與驗證就宣稱預測軸承壽命。分開raw data、feature、alert與maintenance outcome，才能追查誤警報。

數位分身（digital twin）是與實體資產有資料關聯的模型；尚未接實體時，本專案稱simulator／virtual node較準確。模型的prediction error要量化，不能只以漂亮dashboard當成模型驗證。

### 公開資料閱讀與例題類型

BLE primer是標準組織教學文件；MQTT是規格，並非有統一課後題號的教科書。I1–I7皆為依規格自編的教科書型例題，無冒稱商業教科書原題。[I2][I3]

<a id="s6"></a>

## 6. 練習

1. ATT_MTU=100，notification value理論最大？
2. QoS1能否讓「馬達多轉一次」的side effect自然去重？
3. 10 devices各2samples/s，每筆100bytes，1小時payload量？
4. Retained溫度是否保證現在還有效？

<details><summary>解答</summary>

1. 97 bytes，仍受實際stack與其他限制。
2. 不行；需應用command_id、持久化狀態與執行協定。
3. 10×2×100×3600=7,200,000bytes，約6.87MiB，不含protocol overhead。
4. 不保證；需時間與quality判斷。

</details>

| ID | 來源 | 範圍 |
| --- | --- | --- |
| I1 | [CU ECEE course catalog](https://catalog.colorado.edu/graduate/colleges-schools/engineering-applied-science/programs-study/electrical-computer-and-energy-engineering/) | ECEN5823公開描述 |
| I2 | [Bluetooth SIG LE Primer](https://www.bluetooth.com/bluetooth-le-primer/) | GAP、ATT、GATT與資料操作 |
| I3 | [OASIS MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) | §4.3 QoS、retain、session、Will |
| I4 | [CU Industrial IoT公開概述](https://www.colorado.edu/ali/developing-industrial-internet-things-specialization) | 工業應用學習方向；非校內5773逐堂課程替代 |
| I5 | [Eclipse Mosquitto官方下載](https://mosquitto.org/download/) | 本機broker，macOS安裝入口 |

P4為planned，未宣稱完成BLE硬體、TLS deployment或OTA。
