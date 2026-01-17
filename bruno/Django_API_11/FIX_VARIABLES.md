# 修復 Bruno 變數問題

如果遇到 `getaddrinfo ENOTFOUND {{baseurl}}` 錯誤，請按照以下步驟修復：

## 方法 1：在 Bruno UI 中設定變數（推薦）

1. 開啟 Bruno
2. 開啟集合 `Django_API_11`
3. 點擊集合名稱旁的「...」選單
4. 選擇「Edit Collection」
5. 切換到「Variables」標籤
6. 確認或新增變數：
   - **Name**: `baseUrl` (注意大小寫)
   - **Value**: `http://127.0.0.1:8000`
   - **Type**: `text`
7. 儲存並重新載入集合

## 方法 2：使用完整 URL（臨時解決方案）

如果變數仍然無法使用，可以手動替換所有請求中的 `{{baseUrl}}` 為完整 URL。

### 使用腳本批量替換（macOS/Linux）

在終端機中執行：

```bash
cd /Users/zitingliu/Documents/00-GitHub/django-playground/bruno/Django_API_11

# 備份原始文件
find . -name "*.bru" -exec cp {} {}.bak \;

# 替換變數為完整 URL
find . -name "*.bru" -type f -exec sed -i '' 's|{{baseUrl}}|http://127.0.0.1:8000|g' {} \;
```

### 還原備份（如果需要）

```bash
find . -name "*.bru.bak" | while read f; do mv "$f" "${f%.bak}"; done
```

## 方法 3：檢查 Bruno 版本

確保使用最新版本的 Bruno。舊版本可能不支援集合變數。

下載最新版：https://www.usebruno.com/

## 驗證變數是否生效

1. 開啟任何一個 `.bru` 文件
2. 查看 URL 欄位
3. 如果顯示 `{{baseUrl}}` 而不是實際 URL，表示變數未正確載入
4. 如果顯示 `http://127.0.0.1:8000`，表示變數已正確解析

## 常見問題

**Q: 變數名稱大小寫重要嗎？**  
A: 是的，Bruno 的變數名稱是大小寫敏感的。確保使用 `baseUrl`（不是 `baseurl` 或 `BASEURL`）。

**Q: 為什麼變數在 bruno.json 中定義了還是不工作？**  
A: 有時 Bruno 需要手動在 UI 中設定變數。直接在 Bruno 的集合設定中添加變數通常更可靠。

**Q: 可以為不同環境設定不同的 baseUrl 嗎？**  
A: 可以！在 Bruno 中可以創建多個環境（Environments），每個環境可以有不同的變數值。

