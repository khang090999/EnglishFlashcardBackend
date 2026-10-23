from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

# Absence of a progress row represents an unstudied word.
PROGRESS_STATUSES = (("known", _("Known")), ("review", _("Review")))


class WordProgress(BaseModel):
    """A user's latest grade for a word, shared across all its decks."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="word_progress",
        verbose_name=_("User"),
    )
    word = models.ForeignKey(
        "flashcard.Word",
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name=_("Word"),
    )
    status = models.CharField(
        _("Status"),
        max_length=6,
        choices=PROGRESS_STATUSES,
    )

    class Meta:
        verbose_name = _("Word progress")
        verbose_name_plural = _("Word progress")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "word"),
                name="flashcard_unique_word_progress",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    status__in=[
                        status for status, _label in PROGRESS_STATUSES
                    ],
                ),
                name="flashcard_valid_progress_status",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.word} ({self.status})"
