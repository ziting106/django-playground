from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 前端路由（保留用於向後兼容或管理後台）
    path("practices/", include("apps.practices.urls")),
    path("blog/", include("apps.blog.urls")),
    # API 路由
    path("api/v1/blog/", include("apps.blog.api_urls")),
]
