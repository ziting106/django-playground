import django_filters

from apps.blog.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            "title": ["icontains"],
            "author": ["exact"],
            "tags": ["exact"],  
        }
