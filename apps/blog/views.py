# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
# Create your views here.
from apps.blog.models import Article, Author, Tag


def article_list(request):
    articles = Article.objects.select_related("author").prefetch_related("tags").all()
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, "blog/article_detail.html", {"article": article})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "blog/tag_list.html", {"tags": tags})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})
