from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('helauth/', include('helusers.urls')),
    path('admin/', admin.site.urls),
]
