from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Word(BaseModel):
    """Vocabulary shared by deck memberships and tracked by word identity."""

    english = models.CharField(
        _("English"),
        max_length=500,
        validators=[RegexValidator(r"\S", _("Enter nonblank English text."))],
    )
    phonetic = models.CharField(_("Phonetic"), max_length=500, blank=True)
    vietnamese = models.CharField(
        _("Vietnamese"),
        max_length=500,
        validators=[
            RegexValidator(r"\S", _("Enter nonblank Vietnamese text.")),
        ],
    )
    example = models.TextField(_("Example"), blank=True)

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(english=""),
                name="flashcard_word_nonempty_english",
            ),
            models.CheckConstraint(
                condition=~models.Q(vietnamese=""),
                name="flashcard_word_nonempty_vietnamese",
            ),
        ]

    def __str__(self) -> str:
        return self.english
