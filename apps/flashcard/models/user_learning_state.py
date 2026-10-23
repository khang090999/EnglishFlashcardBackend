from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class UserLearningState(BaseModel):
    """A lazily created pointer to the last deck opened by a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_state",
        verbose_name=_("User"),
    )
    last_deck = models.ForeignKey(
        "flashcard.Deck",
        on_delete=models.SET_NULL,
        related_name="learning_states",
        null=True,
        blank=True,
        verbose_name=_("Last deck"),
    )

    class Meta:
        verbose_name = _("User learning state")
        verbose_name_plural = _("User learning states")

    def __str__(self) -> str:
        return str(self.user)
