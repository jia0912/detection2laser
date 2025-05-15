# 黑水虻計畫 - YOLO垃圾物件辨識與雷射標記系統

該專案致力於使用 YOLO 模型進行垃圾物件的辨識，並將辨識到的物件座標轉換為振鏡座標，以實現雷射標記。
專案分成物件偵測與雷射投影，這裡的程式主要負責相機座標與振鏡座標的校正及轉換，並進行物件座標的測試和通訊。

---

## 功能介紹

* **YOLO物件辨識**：使用 YOLO 模型進行垃圾物件的辨識，並提取其影像座標。
* **相機與振鏡座標校正**：透過互動式校正程序，確保兩者的座標系統能準確對應。
* **座標轉換與雷射標記**：將 YOLO 所得影像座標轉換為振鏡座標並進行投影標記。

---

## 執行環境

* Python 3.x
* 列於 `requirements.txt` 中的依賴套件

---

## 使用流程 (How to use)

### 1. 安裝依賴：

先安裝必要的 Python 套件：

```bash
pip install -r requirements.txt
```

### 2. 使用 `calbration.py` 進行雷射與影像座標校正：

此步驟可讓相機座標對應至振鏡控制座標。執行下列指令後，請使用滑鼠點選畫面中的雷射點，系統會自動建立對應關係。

```bash
python calbration.py
```

完成後會產出以下檔案：

* `calibration_data.csv`：儲存點對應資料
* `transformation_matrix.npy`：座標轉換矩陣

### 3. （可選）確認校正結果：

執行以下指令以視覺化對應校正結果，檢查影像點與振鏡點是否正確對應。

```bash
python transTest.py
```

⚠️ *此步驟僅在需要確認或重新校正時執行。*

### 4. 執行雷射投影程式：

啟動伺服器以接收辨識結果並控制振鏡投影。

```bash
python receiveProjection.py
```

### 5. 物件偵測程式運行：

啟動 YOLO 偵測端（另行執行），並於偵測端輸入伺服器的 IP 與 PORT。 當伺服器啟動成功後，Terminal 會顯示：

```
伺服器已啟動，等待連線 (192.168.87.110:5000)...
```

請將該 IP 與 Port 設定至物件偵測端，傳送影像座標供投影使用。

---

## Project Structure

```
.
├── calibration_images/                # 用於相機校正的影像資料夾
├── calbration.py                      # 校正相機與振鏡的對應座標
├── calibration_data.csv               # 儲存手動點選對應點的紀錄
├── README.md                          # 說明文件
├── receiveProjection.py               # 伺服器端，接收影像座標並控制雷射投影
├── requirements.txt                   # Python 依賴套件列表
├── simulationSend.py                  # 模擬影像座標傳送行為
├── transformation_matrix.npy          # 儲存座標轉換矩陣
└── transTest.py                       # 確認校正結果的視覺化工具
```

---

## 注意事項

* **相機與振鏡解析度需固定**：校正完成後，避免調整鏡頭參數或振鏡解析度，以免影響轉換準確性。
* **IP 與 PORT 必須一致**：請確認 YOLO 偵測端與 `receiveProjection.py` 的 IP 與 PORT 設定一致，才能成功傳輸資料。


## ✨ Author

* Developed by [jiajun]  
* GitHub: [@jia0912](https://github.com/jia0912)