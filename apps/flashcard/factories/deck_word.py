import factory

from .. import models
from .deck import DeckFactory
from .word import WordFactory


class DeckWordFactory(factory.django.DjangoModelFactory[models.DeckWord]):
    """Generate memberships with distinct positions, including shared decks."""

    deck = factory.SubFactory(DeckFactory)
    word = factory.SubFactory(WordFactory)
    position = factory.Sequence(lambda number: number)

    class Meta:
        model = models.DeckWord
