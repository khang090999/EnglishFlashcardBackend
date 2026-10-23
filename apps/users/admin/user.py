from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin

from .. import models


@admin.register(models.User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""

    ordering = ("-id",)
    readonly_fields = ("last_login",)
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_display_links = ("email",)
    list_filter = ("role", *DjangoUserAdmin.list_filter)
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "last_login",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
