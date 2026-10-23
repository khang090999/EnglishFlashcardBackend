import enum

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Deck(BaseModel):
    """A starter or custom vocabulary set with ordered, shared words."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        related_name="created_decks",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    title = models.CharField(
        _("Title"),
        max_length=80,
        validators=[RegexValidator(r"\S", _("Enter a nonblank title."))],
    )
    description = models.TextField(_("Description"), blank=True)

    class Level(models.TextChoices):
        """Represent the CEFR proficiency level of a deck."""

        A1 = enum.auto(), _("A1")
        A2 = enum.auto(), _("A2")
        B1 = enum.auto(), _("B1")
        B2 = enum.auto(), _("B2")
        C1 = enum.auto(), _("C1")
        C2 = enum.auto(), _("C2")

    level = models.CharField(
        _("Level"),
        max_length=max(map(len, Level.values)),
        choices=Level.choices,
        db_index=True,
    )
    topic = models.CharField(_("Topic"), max_length=100, blank=True)
    color = models.CharField(_("Color"), max_length=50, blank=True)
    icon = models.CharField(_("Icon"), max_length=50, blank=True)
    is_custom = models.BooleanField(_("Custom"), default=False)
    words = models.ManyToManyField(
        "flashcard.Word",
        through="flashcard.DeckWord",
        related_name="decks",
        verbose_name=_("Words"),
    )

    class Meta:
        verbose_name = _("Deck")
        verbose_name_plural = _("Decks")
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(is_custom=True, created_by__isnull=False)
                    | models.Q(is_custom=False, created_by__isnull=True)
                ),
                name="flashcard_deck_creator_matches_custom",
            ),
            models.CheckConstraint(
                condition=~models.Q(title=""),
                name="flashcard_deck_nonempty_title",
            ),
        ]

    def __str__(self) -> str:
        return self.title

    def clean_created_by(self) -> None:
        """Attach ownership validation errors to the creator field in forms."""
        if self.is_custom and self.created_by_id is None:
            raise ValidationError(_("Custom decks require a creator."))
        if not self.is_custom and self.created_by_id is not None:
            raise ValidationError(_("Starter decks cannot have a creator."))
