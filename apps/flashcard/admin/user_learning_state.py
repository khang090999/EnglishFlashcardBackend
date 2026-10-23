from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import UserLearningState


@admin.register(UserLearningState)
class UserLearningStateAdmin(BaseAdmin):
    """Manage each user's resume-study pointer."""

    list_display = ("id", "user", "last_deck", "modified")
    search_fields = ("user__email", "last_deck__title")
    autocomplete_fields = ("user", "last_deck")
    list_select_related = ("user", "last_deck")
    ordering = ("-modified", "-pk")
    fieldsets = ((None, {"fields": ("user", "last_deck")}),)
