from django.contrib import admin
from django.urls import include, path, re_path

from users.views import MyUserDataView

from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("api/v1/myuserdata/", MyUserDataView.as_view()),
    path("", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("admin/", admin.site.urls),
]
