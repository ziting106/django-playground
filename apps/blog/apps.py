"""
Django App 配置（App Configuration）

每個 Django App 都有一個配置類別，用來定義 App 的行為和設定。
這個檔案通常不需要修改，除非需要自訂 App 的初始化行為。

AppConfig 的用途：
1. 定義 App 的名稱和標籤
2. 設定 App 的預設行為
3. 在 App 啟動時執行初始化程式碼（ready() 方法）
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Blog App 配置類別
    
    這個類別定義了 blog app 的配置。
    在 settings.py 的 INSTALLED_APPS 中，可以指定使用這個配置類別。
    """
    
    # default_auto_field：定義模型的主鍵欄位類型
    # BigAutoField：64 位元的自動遞增整數（適合大型專案）
    # 如果不設定，Django 3.2+ 預設使用 BigAutoField
    # 舊版本預設使用 AutoField（32 位元）
    default_auto_field = "django.db.models.BigAutoField"
    
    # name：App 的完整 Python 路徑
    # 必須與 App 的目錄結構一致
    name = "apps.blog"
    
    # 其他常用的屬性：
    # - verbose_name：App 的顯示名稱（用於 Admin 等地方）
    # - label：App 的簡短標籤（預設為 name 的最後一部分）
    
    # 如果需要 App 啟動時執行初始化程式碼，可以覆寫 ready() 方法：
    # def ready(self):
    #     import apps.blog.signals  # 例如：載入訊號處理器