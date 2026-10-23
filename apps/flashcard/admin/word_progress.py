from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import WordProgress


@admin.register(WordProgress)
class WordProgressAdmin(BaseAdmin):
    """Inspect and update a user's latest word grades."""

    list_display = ("id", "user", "word", "status", "modified")
    list_filter = ("status",)
    search_fields = ("user__email", "word__english", "word__vietnamese")
    autocomplete_fields = ("user", "word")
    list_select_related = ("user", "word")
    ordering = ("-modified", "-pk")
    fieldsets = ((None, {"fields": ("user", "word", "status")}),)
