import json
from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from social_django.models import UserSocialAuth

from .models import User, UserData


class UserSocialAuthInline(admin.StackedInline):
    model = UserSocialAuth
    readonly_fields = ["get_extra_data"]
    exclude = ["extra_data"]
    extra = 0

    def get_extra_data(self, obj=None):
        if not obj or not obj.extra_data:
            return ""

        return mark_safe(f"<pre>{escape(json.dumps(obj.extra_data, indent=4))}</pre>")

    get_extra_data.short_description = _("Extra data")


class UserDataInline(admin.StackedInline):
    model = UserData
    can_delete = False
    verbose_name_plural = "User data"


@admin.register(User)
class ExampleUserAdmin(UserAdmin):
    list_display = ("uuid",) + UserAdmin.list_display
    inlines = (UserDataInline, UserSocialAuthInline)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets = deepcopy(fieldsets)
            fieldsets[1][1]["fields"] += ("uuid",)
            permission_fields = list(fieldsets[2][1]["fields"])
            fieldsets[2][1]["fields"] = tuple(permission_fields) + (
                "department_name",
                "ad_groups",
            )
        return fieldsets
