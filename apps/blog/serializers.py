from rest_framework import serializers
from apps.blog.models import Article, Author, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "email", "bio", "created_at"]


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True, required=False
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source="tags", many=True, write_only=True, required=False
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
            "is_published",
            "author",
            "author_id",
            "tags",
            "tag_ids",
        ]
        read_only_fields = ["created_at", "updated_at"]

