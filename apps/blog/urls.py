"""
Django URL 路由配置（URL Configuration）

URL 路由是 Django 的入口點，定義了哪些 URL 對應到哪些 View。

URL 解析流程：
1. 使用者訪問 URL（如 /blog/articles/）
2. Django 從根 URLconf（core/urls.py）開始匹配
3. 找到匹配的 include，繼續匹配子 URLconf（本檔案）
4. 找到匹配的 path，呼叫對應的 View 函數
5. View 處理請求並返回回應

URL 命名空間（app_name）：
- 用來避免不同 app 之間的 URL 名稱衝突
- 使用方式：reverse("blog:article_list") 或 {% url "blog:article_list" %}
"""

from django.urls import path

from apps.blog import views

# app_name：定義 URL 命名空間
# 這樣可以在其他地方的模板或程式碼中使用 "blog:article_list" 來引用這個 URL
app_name = "blog"

# urlpatterns：URL 模式列表
# Django 會按照順序匹配這些模式，找到第一個匹配的就停止
urlpatterns = [
    # path()：定義一個 URL 模式
    # 第一個參數：URL 路徑（相對路徑，不包含前綴）
    # 第二個參數：對應的 View 函數或類別
    # name：URL 的名稱，用來在程式碼中引用這個 URL
    
    # 標籤列表：/blog/tags/
    path("tags/", views.tag_list, name="tag_list"),
    
    # 作者列表：/blog/authors/
    path("authors/", views.author_list, name="author_list"),
    
    # 文章列表：/blog/articles/
    path("articles/", views.article_list, name="article_list"),
    
    # 建立文章：/blog/articles/create/
    path("articles/create/", views.article_create, name="article_create"),
    
    # 文章詳情：/blog/articles/<id>/
    # <int:id>：URL 參數，int 表示只接受整數，id 是參數名稱
    # 這個參數會傳給 View 函數作為關鍵字參數
    path("articles/<int:id>/", views.article_detail, name="article_detail"),
    
    # 編輯文章：/blog/articles/<id>/edit/
    path("articles/<int:id>/edit/", views.article_edit, name="article_edit"),
    
    # 刪除文章：/blog/articles/<id>/delete/
    path("articles/<int:id>/delete/", views.article_delete, name="article_delete"),
]

# URL 參數類型：
# - <int:id>：整數
# - <str:name>：字串（不包含斜線）
# - <slug:slug>：URL 友好的字串（只包含字母、數字、連字號、底線）
# - <uuid:uuid>：UUID 格式
# - <path:path>：字串（可以包含斜線）
