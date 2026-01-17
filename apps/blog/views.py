"""
Django Views（視圖）

Views 是 Django 中處理 HTTP 請求的核心組件。
每個 View 函數接收一個 request 物件，並返回一個 HttpResponse 物件。

Django 的請求處理流程：
1. 使用者發送 HTTP 請求 → URL 路由（urls.py）
2. URL 路由找到對應的 View 函數
3. View 函數處理請求（查詢資料庫、處理表單等）
4. View 函數返回 HttpResponse（通常是渲染模板後的 HTML）

本檔案包含傳統的 Django Views（使用函數式視圖），
與 drf_views.py 中的 APIView（類別式視圖）不同。
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from apps.blog.filters import ArticleFilter
from apps.blog.forms import ArticleForm
from django.contrib.auth.decorators import permission_required
from apps.blog.models import Article, Author, Tag


def article_list(request):
    """
    文章列表視圖
    
    功能：顯示所有文章的列表，並支援篩選功能
    
    參數：
    - request：HTTP 請求物件，包含 GET 參數、POST 資料、使用者資訊等
    
    處理流程：
    1. 使用 ArticleFilter 處理 GET 參數（如搜尋關鍵字、作者篩選等）
    2. select_related("author")：優化查詢，減少資料庫查詢次數（JOIN 查詢）
    3. prefetch_related("tags")：優化多對多關係的查詢
    4. 將篩選結果傳給模板渲染
    
    優化說明：
    - select_related：用於一對一或一對多關係，使用 SQL JOIN 一次查詢
    - prefetch_related：用於多對多關係，使用額外的 SQL 查詢但減少查詢次數
    """
    # ArticleFilter：使用 django-filter 套件來處理篩選
    # request.GET or None：如果有 GET 參數就使用，否則為 None
    filter_ = ArticleFilter(
        request.GET or None,
        # queryset：指定要篩選的資料集
        # select_related("author")：預先載入作者資訊，避免 N+1 查詢問題
        # prefetch_related("tags")：預先載入標籤資訊
        queryset=Article.objects.select_related("author").prefetch_related("tags"),
    )
    # render：渲染模板並返回 HttpResponse
    # 第一個參數：request 物件
    # 第二個參數：模板路徑（相對於 templates 資料夾）
    # 第三個參數：傳給模板的上下文資料（字典格式）
    return render(request, "blog/article_list.html", {"filter": filter_})


# ============================================================================
# 以下是被註解掉的舊版本實作，保留作為學習參考
# ============================================================================

# 手寫查詢版本（不使用 django-filter）
# def article_list(request):
#     """
#     手動處理篩選的版本
#     這個版本不使用 django-filter，而是手動從 GET 參數取得篩選條件
#     """
#     # request.GET：取得 URL 中的查詢參數（如 ?search=django&author=1）
#     # .get("search", "")：取得 search 參數，如果不存在則返回空字串
#     search = request.GET.get("search", "")
#     author_id = request.GET.get("author", "")
#
#     # 建立基本 QuerySet（尚未執行資料庫查詢，只是定義查詢條件）
#     articles = Article.objects.select_related("author").prefetch_related("tags")
#
#     # filter：根據條件篩選資料
#     # title__icontains：不區分大小寫的包含查詢（LIKE '%search%'）
#     if search:
#         articles = articles.filter(title__icontains=search)
#
#     # author_id：直接使用外鍵的 ID 欄位進行查詢
#     if author_id:
#         articles = articles.filter(author_id=author_id)
#
#     return render(
#         request, "blog/article_list.html", {"articles": articles, "search": search}
#     )

# 沒有查詢功能的簡單版本
# def article_list(request):
#     """
#     最簡單的版本，只顯示所有文章，沒有篩選功能
#     """
#     articles = Article.objects.select_related("author").prefetch_related("tags").all()
#     return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, id):
    """
    文章詳情視圖
    
    功能：顯示單一文章的詳細內容
    
    參數：
    - request：HTTP 請求物件
    - id：從 URL 中取得文章 ID（由 urls.py 中的 <int:id> 提供）
    
    get_object_or_404：
    - 嘗試從資料庫取得文章，如果找不到則返回 404 錯誤頁面
    - 比直接使用 Article.objects.get(id=id) 更安全，因為會自動處理不存在的狀況
    """
    article = get_object_or_404(Article, id=id)
    return render(request, "blog/article_detail.html", {"article": article})


def tag_list(request):
    """
    標籤列表視圖
    
    功能：顯示所有標籤
    """
    # .all()：取得所有標籤（返回 QuerySet）
    tags = Tag.objects.all()
    return render(request, "blog/tag_list.html", {"tags": tags})


def author_list(request):
    """
    作者列表視圖
    
    功能：顯示所有作者
    """
    authors = Author.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


# ============================================================================
# 文章 CRUD 操作（Create, Read, Update, Delete）
# ============================================================================

@permission_required("blog.add_article", raise_exception=True)
def article_create(request):
    """
    建立文章視圖
    
    功能：處理新文章的建立
    
    權限控制：
    - @permission_required：裝飾器，確保使用者有建立文章的權限
    - "blog.add_article"：權限名稱（格式：app_name.permission_name）
    - raise_exception=True：如果沒有權限，拋出 403 錯誤而不是重定向到登入頁
    
    處理流程：
    1. 如果是 GET 請求：顯示空表單
    2. 如果是 POST 請求：驗證表單資料
       - 驗證通過：儲存文章並重定向到文章詳情頁
       - 驗證失敗：顯示表單和錯誤訊息
    """
    # request.POST or None：
    # - 如果是 POST 請求，request.POST 包含表單資料
    # - 如果是 GET 請求，request.POST 為空，使用 None 顯示空表單
    form = ArticleForm(request.POST or None)
    
    # is_valid()：驗證表單資料是否符合規則（定義在 forms.py 中）
    if form.is_valid():
        # form.save()：將表單資料儲存到資料庫，返回建立的 Article 物件
        article = form.save()
        # messages：Django 的訊息框架，用來顯示成功/錯誤訊息給使用者
        # success：成功訊息，會在下次請求時顯示
        messages.success(request, f"文章「{article.title}」已成功建立。")
        # redirect：重定向到指定頁面
        # "blog:article_detail"：URL 名稱（定義在 urls.py 中）
        # id=article.id：傳遞文章 ID 作為 URL 參數
        return redirect("blog:article_detail", id=article.id)

    # 如果表單驗證失敗或這是 GET 請求，顯示表單頁面
    return render(request, "blog/article_create.html", {"form": form})


@permission_required("blog.change_article", raise_exception=True)
def article_edit(request, id):
    """
    編輯文章視圖
    
    功能：處理文章的更新
    
    與 article_create 的差異：
    - 需要先取得要編輯的文章（使用 id 參數）
    - 表單初始化時傳入 instance=article，會預填現有資料
    """
    # 取得要編輯的文章，如果不存在則返回 404
    article = get_object_or_404(Article, id=id)
    
    # instance=article：將現有文章資料填入表單
    form = ArticleForm(request.POST or None, instance=article)
    
    if form.is_valid():
        # form.save()：更新文章資料
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", id=article.id)

    # 傳遞 article 物件給模板，以便顯示文章資訊
    return render(request, "blog/article_edit.html", {"form": form, "article": article})


# ============================================================================
# 刪除文章的兩種實作方式（安全 vs 不安全）
# ============================================================================

# 危險刪除示範（不建議使用）
# def article_delete(request, id):
#     """
#     不安全的刪除方式
#     問題：
#     1. 沒有權限檢查
#     2. GET 請求也可以刪除（違反 RESTful 原則）
#     3. 沒有確認頁面，容易誤刪
#     4. 沒有 CSRF 保護（雖然 Django 預設有，但最好明確使用 POST）
#     """
#     article = get_object_or_404(Article, id=id)
#     article.delete()  # 直接刪除，沒有確認
#     return redirect("blog:article_list")


@permission_required("blog.delete_article", raise_exception=True)
def article_delete(request, id):
    """
    安全刪除視圖（推薦使用）
    
    功能：處理文章的刪除，包含確認步驟
    
    安全措施：
    1. 權限檢查：只有有刪除權限的使用者才能刪除
    2. 確認機制：先顯示確認頁面，使用者確認後才刪除
    3. 只接受 POST 請求：防止 CSRF 攻擊和誤刪
    4. 成功訊息：刪除後顯示確認訊息
    """
    article = get_object_or_404(Article, id=id)

    # 只處理 POST 請求（確認刪除）
    if request.method == "POST":
        # delete()：從資料庫中刪除物件
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    # GET 請求：顯示確認刪除頁面
    return render(request, "blog/article_delete.html", {"article": article})
