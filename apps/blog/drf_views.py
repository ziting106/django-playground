"""
Django REST Framework API Views（API 視圖）

本檔案使用 DRF 的 APIView 來建立 RESTful API。
與傳統的 Django Views（views.py）不同，這些 Views 返回 JSON 格式的資料，
而不是 HTML 頁面。

RESTful API 的 HTTP 方法對應：
- GET：取得資源（列表或單一資源）
- POST：建立新資源
- PUT/PATCH：更新資源
- DELETE：刪除資源

APIView vs 函數式視圖：
- APIView：類別式視圖，可以定義多個 HTTP 方法（get, post, put, delete）
- 函數式視圖：使用 @api_view 裝飾器，每個函數處理一種 HTTP 方法
"""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Article
from apps.blog.serializers import ArticleSerializer


@extend_schema(
    summary="取得文章列表",
    description="取得所有文章的列表",
    tags=["文章"],
)
# 使用 APIView 來處理文章列表的 GET 和 POST 請求    
class ArticleListAPIView(APIView):
    """
    文章列表 API 視圖
    
    這個類別處理文章列表的 GET 和 POST 請求。
    繼承自 APIView，可以定義不同的 HTTP 方法處理函數。
    """

    def get(self, request):
        """
        處理 GET 請求：取得所有文章列表
        
        參數：
        - request：DRF 的 Request 物件，包含請求資訊
        
        處理流程：
        1. 從資料庫取得所有文章
        2. 使用 Serializer 將文章物件轉換為 JSON 格式
        3. 返回 JSON 回應
        
        返回格式：
        [
            {
                "id": 1,
                "title": "文章標題",
                "content": "文章內容",
                ...
            },
            ...
        ]
        """
        # 取得所有文章（QuerySet）
        articles = Article.objects.all()
        
        # Serializer 將多個物件序列化為 JSON
        # many=True：表示要序列化多個物件（列表）
        serializer = ArticleSerializer(articles, many=True)
        
        # Response：DRF 的 HTTP 回應類別，會自動將資料轉換為 JSON
        # serializer.data：序列化後的資料（字典或列表）
        return Response(serializer.data)

    @extend_schema(
        summary="新增文章",
        description="建立新文章",
        tags=["文章"],
    )
    def post(self, request):
        """
        處理 POST 請求：建立新文章
        
        參數：
        - request：包含 JSON 格式的文章資料（在 request.data 中）
        
        處理流程：
        1. 使用 Serializer 驗證輸入資料
        2. 如果驗證通過，建立文章物件
        3. 返回新建立的文章資料
        
        請求範例：
        POST /api-drf/blog/articles
        {
            "title": "新文章標題",
            "content": "文章內容",
            "is_published": false
        }
        """
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果驗證失敗，返回錯誤訊息
        # serializer.errors：包含所有驗證錯誤的字典
        # status=400：HTTP 狀態碼 400（Bad Request）
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="文章詳情",
    description="取得、更新或刪除指定文章",
    tags=["文章"],
)

# 使用 APIView 來處理單一文章的 GET、PUT、DELETE 請求
class ArticleDetailAPIView(APIView):
    """
    文章詳情 API 視圖
    
    這個類別處理單一文章的 GET、PUT、DELETE 請求。
    pk 參數從 URL 中取得（定義在 drf_urls.py 中）。
    """
    def get_object(self, pk):
        return Article.objects.get(pk=pk)

    def get(self, request, pk):
        """
        處理 GET 請求：取得單一文章詳情
        
        參數：
        - request：HTTP 請求物件
        - pk：文章的主鍵（Primary Key），從 URL 中取得
        
        注意：目前這個方法只是返回簡單訊息，實際應該：
        1. 從資料庫取得文章：article = get_object_or_404(Article, pk=pk)
        2. 使用 Serializer 序列化：serializer = ArticleSerializer(article)
        3. 返回資料：return Response(serializer.data)
        """
        try:
            article = self.get_object(pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response(
                {"detail": f"找不到 ID 為 {pk} 的文章"}, status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="更新文章",
        description="更新指定文章",
        tags=["文章"],
    )
    def put(self, request, pk):
        """
        處理 PUT 請求：完整更新文章（需要提供所有欄位）
        
        參數：
        - request：包含要更新的資料
        - pk：要更新的文章 ID
        
        注意：目前這個方法只是返回簡單訊息，實際應該：
        1. 取得文章：article = get_object_or_404(Article, pk=pk)
        2. 驗證資料：serializer = ArticleSerializer(article, data=request.data)
        3. 儲存更新：if serializer.is_valid(): serializer.save()
        4. 返回更新後的資料
        
        PUT vs PATCH：
        - PUT：完整更新，需要提供所有欄位
        - PATCH：部分更新，只需要提供要更新的欄位
        """
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response({"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article, data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="刪除文章",
        description="刪除指定文章",
        tags=["文章"],
    )
    def delete(self, request, pk):
        """
        處理 DELETE 請求：刪除文章
        
        參數：
        - request：HTTP 請求物件
        - pk：要刪除的文章 ID
        
        注意：目前這個方法只是返回狀態碼，實際應該：
        1. 取得文章：article = get_object_or_404(Article, pk=pk)
        2. 刪除文章：article.delete()
        3. 返回 204 狀態碼（No Content，表示成功但沒有內容返回）
        
        HTTP_204_NO_CONTENT：HTTP 狀態碼 204，表示請求成功但沒有內容返回
        這是 RESTful API 中刪除操作常用的狀態碼
        """
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)