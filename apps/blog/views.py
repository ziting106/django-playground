from django.shortcuts import render

# Create your views here.
from apps.blog.models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, id):
    article = Article.objects.get(id=id)
    return render(request, "blog/article_detail.html", {"article": article})
