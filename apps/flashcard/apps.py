from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlashcardAppConfig(AppConfig):
    """Configure vocabulary and per-user learning records."""

    name = "apps.flashcard"
    verbose_name = _("Flashcards")
