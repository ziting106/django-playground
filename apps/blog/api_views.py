from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.blog.models import Article, Author, Tag
from apps.blog.serializers import (
    ArticleSerializer,
    AuthorSerializer,
    TagSerializer,
)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article API 端點
    提供文章的 CRUD 操作
    """

    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Article.objects.all().order_by("-created_at")
        # 可選：只返回已發布的文章
        is_published = self.request.query_params.get("published", None)
        if is_published == "true":
            queryset = queryset.filter(is_published=True)
        return queryset

    @action(detail=False, methods=["get"])
    def published(self, request):
        """獲取所有已發布的文章"""
        published_articles = self.queryset.filter(is_published=True)
        serializer = self.get_serializer(published_articles, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Author API 端點
    提供作者的 CRUD 操作
    """

    queryset = Author.objects.all().order_by("-created_at")
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def articles(self, request, pk=None):
        """獲取特定作者的所有文章"""
        author = self.get_object()
        articles = Article.objects.filter(author=author)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    Tag API 端點
    提供標籤的 CRUD 操作
    """

    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def articles(self, request, pk=None):
        """獲取特定標籤的所有文章"""
        tag = self.get_object()
        articles = Article.objects.filter(tags=tag)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

