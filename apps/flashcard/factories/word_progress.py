import factory

from apps.users.factories import UserFactory

from .. import models
from ..models.word_progress import PROGRESS_STATUSES
from .word import WordFactory


class WordProgressFactory(
    factory.django.DjangoModelFactory[models.WordProgress],
):
    """Generate a learner's latest grade for a word."""

    user = factory.SubFactory(UserFactory)
    word = factory.SubFactory(WordFactory)
    status = factory.Iterator([status for status, _label in PROGRESS_STATUSES])

    class Meta:
        model = models.WordProgress
