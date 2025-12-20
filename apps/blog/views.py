from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.blog.forms import ArticleForm

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


# Create Article
def article_create(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功建立。")
        return redirect("blog:article_detail", id=article.id)

    return render(request, "blog/article_create.html", {"form": form})


# Edit Article
def article_edit(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


# 危險刪除示範Delete
# def article_delete(request, id):
#     article = get_object_or_404(Article, id=id)
#     article.delete()
#     return redirect("blog:article_list")


# 安全刪除示範Delete
def article_delete(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})
