# Django Playground API - Bruno 測試集合

這個 Bruno 集合包含了 Django Playground 專案的所有 API 端點測試。

## 📁 目錄結構

```
Django_API_11/
├── 01_DRF_API/              # Django REST Framework API
│   └── 01_Articles/         # 文章相關 API
├── 02_Blog_Views/            # Blog 傳統 Views
├── 03_Practices/             # Practices 練習端點
├── 04_Auth/                  # 認證相關端點
├── 05_API_Documentation/     # API 文檔端點
└── bruno.json                # Bruno 集合配置
```

## 🚀 使用方式

### 1. 開啟 Bruno

1. 安裝 [Bruno](https://www.usebruno.com/)
2. 在 Bruno 中開啟此資料夾：`bruno/Django_API_11/`

### 2. 設定環境變數

集合中已定義 `baseUrl` 變數，預設為 `http://127.0.0.1:8000`

**在 Bruno 中設定變數：**

1. 在 Bruno 中開啟集合後，點擊集合名稱旁的「...」選單
2. 選擇「Edit Collection」
3. 在「Variables」標籤中，確認 `baseUrl` 變數已設定為 `http://127.0.0.1:8000`
4. 如果變數不存在，點擊「Add Variable」新增：
   - Name: `baseUrl`
   - Value: `http://127.0.0.1:8000`
   - Type: `text`

**如果遇到 `getaddrinfo ENOTFOUND {{baseurl}}` 錯誤：**

1. **檢查變數名稱大小寫**：確保使用 `{{baseUrl}}`（注意大小寫）
2. **重新載入集合**：關閉並重新開啟 Bruno 集合
3. **手動設定變數**：在 Bruno UI 中手動添加變數
4. **使用完整 URL**：如果變數仍無法使用，可以暫時在每個請求中直接使用完整 URL：
   - 將 `{{baseUrl}}/api-drf/blog/articles` 改為 `http://127.0.0.1:8000/api-drf/blog/articles`

### 3. 啟動 Django 伺服器

```bash
cd /Users/zitingliu/Documents/00-GitHub/django-playground
uv run manage.py runserver
```

### 4. 執行測試

在 Bruno 中選擇要執行的請求，點擊「Send」按鈕。

## 📋 API 端點清單

### 01_DRF_API (REST API)

- **GET** `/api-drf/blog/articles` - 取得文章列表
- **POST** `/api-drf/blog/articles` - 建立新文章
- **GET** `/api-drf/blog/articles/{pk}` - 取得文章詳情
- **PUT** `/api-drf/blog/articles/{pk}` - 更新文章
- **DELETE** `/api-drf/blog/articles/{pk}` - 刪除文章

### 02_Blog_Views

- **GET** `/blog/tags/` - 取得標籤列表
- **GET** `/blog/authors/` - 取得作者列表
- **GET** `/blog/articles/` - 取得文章列表（支援篩選）
- **POST** `/blog/articles/create/` - 建立新文章
- **GET** `/blog/articles/{id}/` - 取得文章詳情
- **POST** `/blog/articles/{id}/edit/` - 編輯文章
- **POST** `/blog/articles/{id}/delete/` - 刪除文章

### 03_Practices

- **GET** `/practices/hello/` - Hello World
- **GET** `/practices/greeting/` - 問候語
- **GET** `/practices/search/?q={keyword}` - 搜尋功能
- **GET** `/practices/products/` - 產品列表（支援查詢參數）
- **GET** `/practices/products/filter/` - 顏色篩選產品
- **GET** `/practices/hello/{name}/` - 個人化問候
- **GET** `/practices/articles/{year}/{month}/{slug}/` - 文章詳情（路徑參數）
- **GET** `/practices/users/{username}/articles/` - 使用者文章列表
- **GET** `/practices/color-filter/` - 顏色篩選
- **GET** `/practices/contact/` - 聯絡表單頁面
- **POST** `/practices/contact/` - 提交聯絡表單
- **GET** `/practices/cart/` - 購物車（使用 Session）

### 04_Auth

- **POST** `/auth/login/` - 使用者登入
- **POST** `/auth/logout/` - 使用者登出
- **POST** `/auth/register/` - 使用者註冊
- **POST** `/auth/password-change/` - 變更密碼
- **POST** `/auth/password-reset/` - 重設密碼請求

### 05_API_Documentation

- **GET** `/api/schema/` - OpenAPI Schema (JSON)
- **GET** `/api/docs/` - Swagger UI
- **GET** `/api/redoc/` - ReDoc 文檔

## ⚠️ 注意事項

### CSRF Token

部分 POST 請求需要 CSRF token，特別是：
- 認證相關端點（登入、註冊、密碼變更等）
- Blog Views 的建立/編輯/刪除操作
- 聯絡表單提交

**取得 CSRF Token 的方式：**
1. 先發送 GET 請求到對應的表單頁面
2. 從回應的 HTML 中提取 CSRF token
3. 在 POST 請求的 `csrfmiddlewaretoken` 欄位中使用該 token

### Session Cookie

需要登入的端點會使用 Session Cookie：
1. 先執行登入請求
2. 從回應的 Headers 中取得 `Set-Cookie: sessionid=...`
3. 在後續請求的 Headers 中添加 `Cookie: sessionid=...`

### 路徑參數

部分端點使用路徑參數，請在 Bruno 中修改 URL：
- `{pk}` 或 `{id}` → 替換為實際的 ID 數字
- `{name}` → 替換為實際的名稱字串
- `{username}` → 替換為實際的使用者名稱
- `{year}`, `{month}`, `{slug}` → 替換為實際的值

## 🔧 自訂設定

### 修改 Base URL

在 Bruno 中：
1. 右鍵點擊集合名稱
2. 選擇「Edit Collection」
3. 修改 `vars` 中的 `baseUrl` 值

### 新增環境變數

可以在 `bruno.json` 的 `vars` 區段新增更多變數，例如：
- `apiKey`: API 金鑰
- `token`: 認證 token
- `userId`: 使用者 ID

## 📚 相關資源

- [Bruno 官方文檔](https://docs.usebruno.com/)
- [Django REST Framework 文檔](https://www.django-rest-framework.org/)
- [Swagger UI](http://127.0.0.1:8000/api/docs/)

