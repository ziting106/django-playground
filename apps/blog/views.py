from django.shortcuts import render

# Create your views here.
from apps.blog.models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})