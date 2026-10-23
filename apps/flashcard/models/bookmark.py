from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Bookmark(BaseModel):
    """A deck saved by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name=_("User"),
    )
    deck = models.ForeignKey(
        "flashcard.Deck",
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name=_("Deck"),
    )

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "deck"),
                name="flashcard_unique_bookmark",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.deck}"
