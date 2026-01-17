"""
Django REST Framework Serializers（序列化器）

Serializer 是 DRF 的核心組件，用來：
1. 將 Python 物件（如 Model 實例）轉換為 JSON 格式（序列化）
2. 將 JSON 資料轉換為 Python 物件並進行驗證（反序列化）
3. 定義 API 的輸入和輸出格式

使用 Serializer 的好處：
- 自動處理資料驗證
- 控制哪些欄位可以輸入/輸出
- 統一 API 的資料格式
"""

from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    """
    文章序列化器（Article Serializer）
    
    這個 Serializer 定義了文章 API 的輸入和輸出格式。
    它告訴 DRF：
    - 哪些欄位可以從 API 接收（輸入）
    - 哪些欄位會從 API 返回（輸出）
    - 每個欄位的驗證規則
    """
    
    # IntegerField：用來處理整數類型的資料
    # read_only=True：這個欄位只在輸出（序列化）時使用，不會接受輸入（反序列化）
    # 因為 id 通常是資料庫自動產生的，所以設為 read_only
    id = serializers.IntegerField(read_only=True)
    
    # CharField：用來處理字串類型的資料
    # max_length：驗證輸入的最大長度，超過會拋出驗證錯誤
    title = serializers.CharField(max_length=200)
    
    # CharField：沒有指定 max_length，表示可以接受任意長度的字串
    content = serializers.CharField()
    
    # BooleanField：用來處理布林值（True/False）
    # default=False：當沒有提供值時，使用 False 作為預設值
    is_published = serializers.BooleanField(default=False)
    
    # PrimaryKeyRelatedField：用來處理外鍵關係
    # read_only=True：只會在輸出時顯示關聯物件的 ID，不接受輸入
    # 例如：輸出時會顯示 created_by: 1（使用者 ID），而不是整個使用者物件
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # DateTimeField：用來處理日期時間
    # read_only=True：建立時間和更新時間通常由系統自動設定，不需要使用者輸入
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """建立新的 Article 物件"""
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新現有的 Article 物件"""
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.save()
        return instance