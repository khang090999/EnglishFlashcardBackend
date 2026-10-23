from django.contrib import admin

from apps.core.admin import BaseAdmin

from ..models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(BaseAdmin):
    """Manage saved decks for each account."""

    list_display = ("id", "user", "deck", "created")
    search_fields = ("user__email", "deck__title")
    autocomplete_fields = ("user", "deck")
    list_select_related = ("user", "deck")
    ordering = ("-created", "-pk")
    fieldsets = ((None, {"fields": ("user", "deck")}),)
