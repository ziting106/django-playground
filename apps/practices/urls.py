from django.urls import path

from apps.practices import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
]
