"""
Django Filter（篩選器）

django-filter 是一個第三方套件，用來簡化 Django 的查詢篩選功能。
它會根據 GET 參數自動產生對應的資料庫查詢。

使用 FilterSet 的好處：
1. 自動處理 URL 查詢參數（如 ?title=django&author=1）
2. 自動產生篩選表單（可選）
3. 減少重複的查詢邏輯
4. 支援多種查詢類型（exact, icontains, gt, lt 等）
"""

import django_filters

from apps.blog.models import Article


class ArticleFilter(django_filters.FilterSet):
    """
    文章篩選器（Article Filter）
    
    這個 FilterSet 定義了可以對文章進行哪些篩選操作。
    繼承自 django_filters.FilterSet。
    
    使用方式：
    在 views.py 中：
    filter_ = ArticleFilter(request.GET, queryset=Article.objects.all())
    articles = filter_.qs  # 取得篩選後的結果
    """
    
    class Meta:
        """
        Meta 類別：定義篩選器的設定
        """
        # model：指定要篩選的模型
        model = Article
        
        # fields：定義哪些欄位可以篩選，以及使用哪些查詢類型
        # 格式：{"欄位名稱": ["查詢類型1", "查詢類型2", ...]}
        fields = {
            # title：標題欄位
            # "icontains"：不區分大小寫的包含查詢（LIKE '%keyword%'）
            # 例如：?title=django 會查詢標題包含 "django" 的文章
            "title": ["icontains"],
            
            # author：作者欄位（外鍵）
            # "exact"：精確匹配（等於）
            # 例如：?author=1 會查詢作者 ID 為 1 的文章
            "author": ["exact"],
            
            # tags：標籤欄位（多對多關係）
            # "exact"：精確匹配
            # 例如：?tags=1 會查詢包含標籤 ID 為 1 的文章
            "tags": ["exact"],
        }
        
        # 其他常用的查詢類型：
        # - "iexact"：不區分大小寫的精確匹配
        # - "contains"：區分大小寫的包含查詢
        # - "startswith"：開頭匹配
        # - "endswith"：結尾匹配
        # - "gt"：大於
        # - "gte"：大於等於
        # - "lt"：小於
        # - "lte"：小於等於
        # - "in"：在列表中
        # - "range"：範圍查詢