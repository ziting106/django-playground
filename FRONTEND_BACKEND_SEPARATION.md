# 前後端分離專案說明

本專案已配置為 Django + Angular 前後端分離架構。

## 專案結構

```
django-playground/
├── apps/                    # Django 應用程式
│   ├── blog/               # 部落格應用
│   │   ├── api_views.py    # API 視圖集
│   │   ├── api_urls.py     # API 路由
│   │   └── serializers.py  # API 序列化器
│   └── practices/          # 練習應用
├── core/                    # Django 核心設定
│   ├── settings.py         # 包含 CORS 和 REST Framework 設定
│   └── urls.py             # 包含 API 路由
└── frontend/                # Angular 前端專案
    └── src/
        ├── app/
        │   ├── components/  # Angular 組件
        │   ├── services/    # Angular 服務
        │   └── models/     # TypeScript 模型
        └── environments/    # 環境配置
```

## 後端 API 端點

### 文章 API
- `GET /api/v1/blog/articles/` - 獲取所有文章
- `GET /api/v1/blog/articles/?published=true` - 獲取已發布的文章
- `GET /api/v1/blog/articles/{id}/` - 獲取單篇文章
- `POST /api/v1/blog/articles/` - 創建文章
- `PUT /api/v1/blog/articles/{id}/` - 更新文章
- `DELETE /api/v1/blog/articles/{id}/` - 刪除文章
- `GET /api/v1/blog/articles/published/` - 獲取所有已發布文章

### 作者 API
- `GET /api/v1/blog/authors/` - 獲取所有作者
- `GET /api/v1/blog/authors/{id}/` - 獲取單個作者
- `GET /api/v1/blog/authors/{id}/articles/` - 獲取作者的所有文章

### 標籤 API
- `GET /api/v1/blog/tags/` - 獲取所有標籤
- `GET /api/v1/blog/tags/{id}/` - 獲取單個標籤
- `GET /api/v1/blog/tags/{id}/articles/` - 獲取標籤的所有文章

## 啟動專案

### 1. 啟動後端 (Django)

```bash
# 安裝依賴（如果還沒安裝）
uv sync

# 運行遷移
uv run manage.py migrate

# 啟動開發伺服器
uv run manage.py runserver
```

後端將在 `http://localhost:8000` 運行

### 2. 啟動前端 (Angular)

```bash
cd frontend

# 安裝依賴（如果還沒安裝）
npm install

# 啟動開發伺服器
npm start
# 或
ng serve
```

前端將在 `http://localhost:4200` 運行

## 配置說明

### CORS 設定

後端的 CORS 設定在 `core/settings.py` 中：

```python
CORS_ALLOW_ALL_ORIGINS = True  # 開發環境
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
```

**注意**：生產環境應將 `CORS_ALLOW_ALL_ORIGINS` 設為 `False`，並只允許特定的來源。

### API 基礎 URL

前端的 API URL 配置在 `frontend/src/environments/environment.ts`：

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1',
};
```

## 測試 API

可以使用以下方式測試 API：

### 使用 curl

```bash
# 獲取所有文章
curl http://localhost:8000/api/v1/blog/articles/

# 獲取已發布的文章
curl http://localhost:8000/api/v1/blog/articles/?published=true
```

### 使用瀏覽器

直接訪問：`http://localhost:8000/api/v1/blog/articles/`

## 前端功能

1. **首頁** (`/`) - 專案介紹
2. **文章列表** (`/articles`) - 顯示所有文章，可篩選已發布文章
3. **文章詳情** (`/articles/:id`) - 顯示單篇文章的詳細內容

## 下一步

1. 添加身份驗證（JWT Token）
2. 添加文章創建/編輯表單
3. 添加分頁功能
4. 添加搜索功能
5. 優化 UI/UX

