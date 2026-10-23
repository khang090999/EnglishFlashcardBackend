import factory

from apps.users.factories import UserFactory

from .. import models
from .deck import DeckFactory


class BookmarkFactory(factory.django.DjangoModelFactory[models.Bookmark]):
    """Generate a learner's saved deck."""

    user = factory.SubFactory(UserFactory)
    deck = factory.SubFactory(DeckFactory)

    class Meta:
        model = models.Bookmark
