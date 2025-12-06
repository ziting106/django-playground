from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.blog.api_views import ArticleViewSet, AuthorViewSet, TagViewSet

# 創建路由器並註冊視圖集
router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"tags", TagViewSet, basename="tag")

# API URL 配置
urlpatterns = [
    path("", include(router.urls)),
]

