from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("admin/", admin.site.urls),
]
