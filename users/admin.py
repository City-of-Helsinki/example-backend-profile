from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserData


class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = "User data"


class ExampleUserAdmin(UserAdmin):
    inlines = (UserDataInline,)


admin.site.register(User, ExampleUserAdmin)
