from django.contrib import admin

from ..models import DeckWord


class DeckWordInline(admin.TabularInline):
    """Edit ordered word memberships from a deck's admin page."""

    model = DeckWord
    fields = ("word", "position")
    autocomplete_fields = ("word",)
    ordering = ("position",)
    extra = 0
