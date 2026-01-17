"""
Django Admin（管理後台）

Django Admin 是 Django 內建的管理介面，可以快速建立資料庫的 CRUD 操作介面。
不需要寫前端程式碼，就能管理資料庫內容。

使用方式：
1. 建立超級使用者：python manage.py createsuperuser
2. 訪問 /admin/ 路徑
3. 登入後即可管理資料

本檔案定義了各個模型在 Admin 中的顯示方式和功能。
"""

from django.contrib import admin

from apps.blog.models import Article, Author, Tag


class ArticleInline(admin.StackedInline):
    """
    文章內聯（Article Inline）
    
    Inline 用來在另一個模型的編輯頁面中直接編輯相關物件。
    例如：在作者編輯頁面中，可以直接新增或編輯該作者的文章。
    
    StackedInline vs TabularInline：
    - StackedInline：垂直堆疊顯示，每個欄位佔一行（適合欄位較多的情況）
    - TabularInline：表格形式顯示，所有欄位在一行（適合欄位較少的情況）
    """
    model = Article  # 要內聯的模型
    extra = 1  # 預設顯示的空表單數量（可以新增的額外物件數）
    fields = ["title", "content", "is_published"]  # 在內聯中顯示的欄位


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    文章管理類別（Article Admin）
    
    使用 @admin.register 裝飾器註冊模型到 Admin。
    等同於：admin.site.register(Article, ArticleAdmin)
    
    這個類別定義了文章在 Admin 中的顯示方式和功能。
    """
    
    # list_display：定義在列表頁面中顯示哪些欄位
    # 可以包含模型欄位、方法、屬性等
    list_display = [
        "title",  # 文章標題
        "author",  # 作者（外鍵會自動顯示關聯物件的 __str__）
        "is_published",  # 是否發布（會顯示為勾選框）
        "created_at",  # 建立時間
        "tag_count",  # 自訂方法（顯示標籤數量）
    ]
    
    # list_filter：在列表頁面右側顯示的篩選器
    # 可以根據這些欄位快速篩選文章
    list_filter = ["is_published", "created_at", "author"]
    
    # search_fields：啟用搜尋功能，可以搜尋這些欄位
    # 支援模糊搜尋（包含查詢）
    search_fields = ["title", "content"]
    
    # ordering：預設排序方式
    # "-created_at"：按建立時間降序（最新的在前）
    # 可以指定多個欄位：["-created_at", "title"]
    ordering = ["-created_at"]
    
    # list_per_page：每頁顯示的記錄數
    list_per_page = 20
    
    # actions：批量操作（在列表頁面選擇多筆記錄後可以執行的操作）
    actions = ["publish_articles", "unpublish_articles"]
    
    # filter_horizontal：多對多關係的選擇介面
    # 會顯示兩個選擇框（可選 | 已選），方便選擇多個標籤
    filter_horizontal = ["tags"]

    @admin.display(description="標籤數量")
    def tag_count(self, obj):
        """
        自訂顯示欄位：計算文章的標籤數量
        
        參數：
        - obj：當前的 Article 物件
        
        @admin.display：裝飾器，定義這個方法在 Admin 中的顯示方式
        - description：欄位標題（顯示在列表頁面的表頭）
        
        返回：標籤的數量
        """
        # obj.tags：取得文章的所有標籤（多對多關係）
        # .count()：計算數量（比 len() 更有效率，因為在資料庫層面計算）
        return obj.tags.count()

    @admin.action(description="發布選中的文章")
    def publish_articles(self, request, queryset):
        """
        批量操作：發布選中的文章
        
        參數：
        - request：HTTP 請求物件
        - queryset：選中的文章 QuerySet
        
        @admin.action：裝飾器，將方法註冊為批量操作
        - description：操作的名稱（顯示在下拉選單中）
        
        使用方式：
        1. 在列表頁面勾選多篇文章
        2. 在「動作」下拉選單中選擇「發布選中的文章」
        3. 點擊「執行」
        """
        # queryset.update()：批量更新，比逐個更新更有效率
        # 返回更新的記錄數
        count = queryset.update(is_published=True)
        # message_user：顯示訊息給使用者
        self.message_user(request, f"成功發布 {count} 篇文章")

    @admin.action(description="取消發布選中的文章")
    def unpublish_articles(self, request, queryset):
        """
        批量操作：取消發布選中的文章
        
        功能與 publish_articles 相同，但將 is_published 設為 False
        """
        count = queryset.update(is_published=False)
        self.message_user(request, f"成功取消發布 {count} 篇文章")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    作者管理類別（Author Admin）
    
    定義作者在 Admin 中的顯示方式。
    """
    
    # list_display：顯示作者的基本資訊和自訂欄位
    list_display = ["name", "email", "created_at", "has_published_articles"]
    
    # inlines：在作者編輯頁面中顯示內聯物件
    # 這樣可以在編輯作者時，同時管理該作者的文章
    inlines = [ArticleInline]

    @admin.display(description="有已發布的文章", boolean=True)
    def has_published_articles(self, obj):
        """
        自訂顯示欄位：檢查作者是否有已發布的文章
        
        參數：
        - obj：當前的 Author 物件
        
        boolean=True：告訴 Admin 這是一個布林值欄位
        - True 會顯示為勾選圖示（✓）
        - False 會顯示為叉號圖示（✗）
        
        返回：True 或 False
        """
        # obj.articles：取得作者的所有文章（透過 ForeignKey 的 related_name）
        # .filter(is_published=True)：篩選已發布的文章
        # .exists()：檢查是否存在（比 .count() > 0 更有效率）
        return obj.articles.filter(is_published=True).exists()


# 簡單註冊：如果不需要自訂 Admin 類別，可以直接註冊
# admin.site.register(Tag) 會使用預設的 Admin 設定
admin.site.register(Tag)
