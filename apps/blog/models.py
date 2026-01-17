"""
Django Models（資料模型）

Models 是 Django ORM（Object-Relational Mapping）的核心，用來定義資料庫的結構。
每個 Model 類別對應資料庫中的一個表格（table），類別中的屬性對應表格中的欄位（column）。

使用方式：
1. 定義 Model 類別，繼承自 models.Model
2. 定義欄位（Field）
3. 執行 makemigrations 建立遷移檔案
4. 執行 migrate 將變更套用到資料庫
"""

from django.db import models


class Author(models.Model):
    """
    作者模型（Author Model）
    
    這個模型用來儲存文章作者的基本資訊。
    對應資料庫中的 blog_author 表格。
    """
    
    # CharField：用來儲存字串，必須指定最大長度
    # max_length：限制欄位的最大字元數
    name = models.CharField(max_length=100)
    
    # EmailField：專門用來儲存電子郵件地址，會自動驗證格式
    # unique=True：確保資料庫中每筆記錄的 email 都是唯一的
    email = models.EmailField(unique=True)
    
    # TextField：用來儲存較長的文字內容，沒有長度限制
    # blank=True：在表單驗證時，此欄位可以為空（但資料庫中仍會儲存空字串）
    bio = models.TextField(blank=True)
    
    # DateTimeField：用來儲存日期和時間
    # auto_now_add=True：只在物件第一次建立時自動設定為當前時間，之後不會改變
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        __str__ 方法：定義物件的字串表示
        
        當你在 Django shell 或 admin 中查看物件時，會顯示這個方法返回的值。
        例如：Author.objects.get(id=1) 會顯示作者名稱而不是 <Author: Author object (1)>
        """
        return self.name


class Tag(models.Model):
    """
    標籤模型（Tag Model）
    
    用來儲存文章標籤，一個標籤可以被多篇文章使用（多對多關係）。
    對應資料庫中的 blog_tag 表格。
    """
    
    # unique=True：確保標籤名稱在資料庫中是唯一的
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """返回標籤名稱作為物件的字串表示"""
        return self.name


class Article(models.Model):
    """
    文章模型（Article Model）
    
    這是 Blog 應用程式的核心模型，用來儲存文章的內容和相關資訊。
    對應資料庫中的 blog_article 表格。
    
    關係說明：
    - 與 Author：多對一關係（Many-to-One），一篇文章只能有一個作者，但一個作者可以有多篇文章
    - 與 Tag：多對多關係（Many-to-Many），一篇文章可以有多個標籤，一個標籤也可以被多篇文章使用
    """
    
    # 文章標題
    title = models.CharField(max_length=200)
    
    # 文章內容，使用 TextField 因為內容可能很長
    content = models.TextField()
    
    # 建立時間：只在物件第一次建立時自動設定
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 更新時間：每次儲存物件時都會自動更新為當前時間
    updated_at = models.DateTimeField(auto_now=True)
    
    # 是否發布：BooleanField 用來儲存 True/False 值
    # default=False：新建立的文章預設為未發布狀態
    is_published = models.BooleanField(default=False)

    # ForeignKey：建立多對一關係
    # 這表示一篇文章只能有一個作者，但一個作者可以有多篇文章
    author = models.ForeignKey(
        Author,  # 關聯到 Author 模型
        # on_delete：定義當關聯的物件被刪除時的行為
        # CASCADE：當作者被刪除時，該作者的所有文章也會被刪除（級聯刪除）
        # PROTECT：如果作者還有文章，則不允許刪除該作者（保護模式）
        # SET_NULL：當作者被刪除時，將文章的 author 欄位設為 NULL（需要 null=True）
        # SET_DEFAULT：當作者被刪除時，將文章的 author 欄位設為預設值（需要 default）
        on_delete=models.CASCADE,
        # related_name：反向關聯的名稱
        # 設定後，可以透過 author.articles 來取得該作者的所有文章
        # 如果不設定，預設會是 article_set
        related_name="articles",
        # null=True：允許資料庫中此欄位為 NULL
        null=True,
        # blank=True：在表單驗證時，此欄位可以為空
        blank=True,
    )

    # ManyToManyField：建立多對多關係
    # 這表示一篇文章可以有多個標籤，一個標籤也可以被多篇文章使用
    tags = models.ManyToManyField(
        Tag,  # 關聯到 Tag 模型
        # related_name：反向關聯的名稱
        # 設定後，可以透過 tag.articles 來取得使用該標籤的所有文章
        related_name="articles",
        # blank=True：在表單驗證時，此欄位可以為空（文章可以沒有標籤）
        blank=True,
    )

    def __str__(self):
        """返回文章標題作為物件的字串表示"""
        return self.title
