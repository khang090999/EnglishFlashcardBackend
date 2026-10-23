from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import Deck
from .deck_word_inline import DeckWordInline


@admin.register(Deck)
class DeckAdmin(BaseAdmin):
    """Manage deck metadata and its ordered vocabulary."""

    list_display = ("id", "title", "level", "topic", "is_custom", "created_by")
    list_display_links = ("title",)
    list_filter = ("level", "is_custom")
    search_fields = ("title", "description", "topic")
    autocomplete_fields = ("created_by",)
    list_select_related = ("created_by",)
    ordering = ("-created", "-pk")
    inlines = (DeckWordInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "level",
                    "topic",
                    "color",
                    "icon",
                    "is_custom",
                    "created_by",
                ),
            },
        ),
    )
