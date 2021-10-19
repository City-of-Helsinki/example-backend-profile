from django.contrib import admin
from django.urls import include, path, re_path

from users.views import ExampleGDPRAPIView, FillMyBirthday, MyUserDataView

from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("api/v1/myuserdata/", MyUserDataView.as_view()),
    path("api/v1/fillmybirthday/", FillMyBirthday.as_view()),
    # In this example, the GDPR URL in the Profile backend should be
    # [scheme, host, and port]/gdpr-api/v1/user/$user_uuid
    path("gdpr-api/v1/user/<uuid:uuid>", ExampleGDPRAPIView.as_view(), name="gdpr_v1"),
    path("", include("social_django.urls", namespace="social")),
    path("helauth/", include("helusers.urls")),
    path("admin/", admin.site.urls),
]
