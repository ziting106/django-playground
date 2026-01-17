"""
Django Forms（表單）

Forms 用來處理 HTML 表單的驗證和渲染。
ModelForm 是基於 Model 自動產生表單的便捷方式。

使用 Forms 的好處：
1. 自動產生 HTML 表單欄位
2. 自動處理資料驗證
3. 統一錯誤訊息顯示
4. 防止 CSRF 攻擊（Django 自動處理）

表單驗證流程：
1. 使用者提交表單（POST 請求）
2. Django 自動驗證基本規則（必填、長度等）
3. 執行自訂驗證方法（clean_<field_name> 和 clean）
4. 如果驗證通過，可以儲存資料
"""

from django import forms

from apps.blog.models import Article


class ArticleForm(forms.ModelForm):
    """
    文章表單（Article Form）
    
    這是一個 ModelForm，會自動根據 Article 模型產生表單欄位。
    繼承自 forms.ModelForm 可以減少重複程式碼。
    """
    
    class Meta:
        """
        Meta 類別：定義表單的元資料
        
        這裡設定表單要使用哪個模型、哪些欄位、標籤、錯誤訊息等。
        """
        # model：指定要使用的模型
        model = Article
        
        # fields：指定表單要包含哪些欄位
        # 只有列在這裡的欄位會出現在表單中
        fields = ["title", "content", "author"]
        
        # labels：定義欄位的顯示標籤（中文）
        # 如果不設定，會使用模型欄位的名稱
        labels = {
            "title": "標題",
            "content": "內容",
            "author": "作者",
        }
        
        # error_messages：自訂錯誤訊息
        # 當驗證失敗時，會顯示這裡定義的訊息
        error_messages = {
            "title": {
                # required：當欄位為空時顯示的錯誤訊息
                "required": "標題不能空白",
                # max_length：當超過最大長度時顯示的錯誤訊息
                # %(limit_value)d 會被替換為實際的最大長度值
                "max_length": "標題最多 %(limit_value)d 字元",
            },
            "content": {
                "required": "內容不能空白",
            },
        }
        
        # widgets：定義欄位的 HTML 輸入元素類型
        # 這裡將 content 欄位設定為多行文字輸入框（Textarea）
        widgets = {
            # attrs：HTML 屬性
            # rows：文字框的行數
            "content": forms.Textarea(attrs={"rows": 10}),
        }

    def clean_title(self):
        """
        自訂驗證：標題欄位驗證
        
        這個方法會在基本驗證（必填、長度等）之後執行。
        方法命名規則：clean_<field_name>
        
        處理流程：
        1. 從 cleaned_data 取得已清理的標題資料
        2. 執行自訂驗證邏輯
        3. 如果驗證失敗，拋出 ValidationError
        4. 如果驗證通過，返回清理後的資料
        
        注意：cleaned_data 只包含通過基本驗證的資料
        """
        # cleaned_data：經過基本驗證和清理後的資料
        title = self.cleaned_data["title"]
        
        # 自訂驗證規則：標題不能包含「測試」字樣
        if "測試" in title:
            error_message = "標題不能包含「測試」"
            # ValidationError：表單驗證錯誤，會顯示在表單中
            raise forms.ValidationError(error_message)

        # 返回清理後的資料（可以進行轉換，如去除空白、轉換大小寫等）
        return title

    def clean(self):
        """
        自訂驗證：跨欄位驗證
        
        這個方法用來驗證多個欄位之間的關係。
        在所有欄位的 clean_<field_name> 方法執行完後才會執行。
        
        使用場景：
        - 驗證兩個欄位不能相同
        - 驗證欄位之間的邏輯關係
        - 需要同時檢查多個欄位的情況
        """
        # super().clean()：呼叫父類別的 clean 方法，確保基本驗證已執行
        cleaned_data = super().clean()
        
        # 從 cleaned_data 取得欄位值
        # .get()：安全取得值，如果不存在則返回 None
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        # 跨欄位驗證：標題和內容不能相同
        if title and content and title == content:
            error_message = "標題與內容不能相同"
            # 不指定欄位的 ValidationError 會顯示在表單頂部
            raise forms.ValidationError(error_message)

        # 返回清理後的資料
        return cleaned_data