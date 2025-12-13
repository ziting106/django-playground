from django.urls import path

from apps.blog import views

app_name = "blog"

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:id>/", views.article_detail, name="article_detail"),
    path("tags/", views.tag_list, name="tag_list"),
    path("authors/", views.author_list, name="author_list"),
]
