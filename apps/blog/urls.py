from django.urls import path

from apps.blog import views

app_name = "blog"

urlpatterns = [
    path("tags/", views.tag_list, name="tag_list"),
    path("authors/", views.author_list, name="author_list"),
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.article_create, name="article_create"),
    path("articles/<int:id>/", views.article_detail, name="article_detail"),
    path("articles/<int:id>/edit/", views.article_edit, name="article_edit"),
    path("articles/<int:id>/delete/", views.article_delete, name="article_delete"),
]
