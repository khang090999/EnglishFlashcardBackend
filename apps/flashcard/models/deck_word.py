from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class DeckWord(BaseModel):
    """Place a word once in a deck at a unique zero-based position."""

    deck = models.ForeignKey(
        "flashcard.Deck",
        on_delete=models.CASCADE,
        related_name="deck_words",
        verbose_name=_("Deck"),
    )
    word = models.ForeignKey(
        "flashcard.Word",
        on_delete=models.PROTECT,
        related_name="deck_words",
        verbose_name=_("Word"),
    )
    position = models.PositiveIntegerField(_("Position"))

    class Meta:
        verbose_name = _("Deck word")
        verbose_name_plural = _("Deck words")
        ordering = ("position",)
        constraints = [
            models.UniqueConstraint(
                fields=("deck", "word"),
                name="flashcard_unique_deck_word",
            ),
            models.UniqueConstraint(
                fields=("deck", "position"),
                name="flashcard_unique_deck_position",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.deck}: {self.word} ({self.position})"
