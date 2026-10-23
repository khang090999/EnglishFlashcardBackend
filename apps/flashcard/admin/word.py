from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import Word


@admin.register(Word)
class WordAdmin(BaseAdmin):
    """Manage vocabulary without merging independent imported words."""

    list_display = ("id", "english", "phonetic", "vietnamese")
    list_display_links = ("english",)
    search_fields = ("english", "vietnamese", "phonetic")
    ordering = ("english", "pk")
    fieldsets = (
        (None, {"fields": ("english", "phonetic", "vietnamese", "example")}),
    )
