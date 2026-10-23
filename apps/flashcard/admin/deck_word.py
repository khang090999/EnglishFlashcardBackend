from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import DeckWord


@admin.register(DeckWord)
class DeckWordAdmin(BaseAdmin):
    """Inspect and edit individual ordered memberships."""

    list_display = ("id", "deck", "word", "position")
    list_filter = ("deck__level",)
    search_fields = ("deck__title", "word__english", "word__vietnamese")
    autocomplete_fields = ("deck", "word")
    list_select_related = ("deck", "word")
    ordering = ("deck_id", "position")
    fieldsets = ((None, {"fields": ("deck", "word", "position")}),)
