"""
Django REST Framework URL 路由配置（DRF URL Configuration）

本檔案定義了 RESTful API 的 URL 路由。
與 urls.py 不同，這裡使用的是 APIView 類別而不是函數式視圖。

RESTful API 的 URL 設計原則：
- 使用名詞（articles）而不是動詞（get_articles）
- 使用 HTTP 方法（GET, POST, PUT, DELETE）來區分操作
- URL 應該清晰表達資源的層級關係
"""

from django.urls import path

from apps.blog.drf_views import ArticleDetailAPIView, ArticleListAPIView

# app_name：URL 命名空間
# 使用 "drf-blog" 來區分傳統 Views 和 API Views
app_name = "drf-blog"

urlpatterns = [
    # 文章列表和建立：/api-drf/blog/articles
    # 這個 URL 對應兩個操作：
    # - GET：取得文章列表（ArticleListAPIView.get）
    # - POST：建立新文章（ArticleListAPIView.post）
    # .as_view()：將 APIView 類別轉換為可呼叫的視圖函數
    path("articles", ArticleListAPIView.as_view(), name="article-list"),
    
    # 文章詳情、更新、刪除：/api-drf/blog/articles/<pk>
    # 這個 URL 對應三個操作：
    # - GET：取得文章詳情（ArticleDetailAPIView.get）
    # - PUT：更新文章（ArticleDetailAPIView.put）
    # - DELETE：刪除文章（ArticleDetailAPIView.delete）
    # <int:pk>：主鍵參數（pk 是 Primary Key 的縮寫，DRF 的慣例）
    path("articles/<int:pk>", ArticleDetailAPIView.as_view(), name="article-detail"),
]

# RESTful API URL 設計範例：
# GET    /api/articles          → 取得所有文章
# POST   /api/articles          → 建立新文章
# GET    /api/articles/1        → 取得 ID 為 1 的文章
# PUT    /api/articles/1        → 完整更新 ID 為 1 的文章
# PATCH  /api/articles/1        → 部分更新 ID 為 1 的文章
# DELETE /api/articles/1        → 刪除 ID 為 1 的文章