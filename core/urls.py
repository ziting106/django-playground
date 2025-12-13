from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("practices/", include("apps.practices.urls")),
    path("blog/", include("apps.blog.urls")),
]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
