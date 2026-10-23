import factory

from apps.users.factories import UserFactory

from .. import models


class DeckFactory(factory.django.DjangoModelFactory[models.Deck]):
    """Generate starter decks or owned decks with is_custom=True."""

    title = factory.Sequence(lambda number: f"Vocabulary deck {number}")
    description = factory.Faker("sentence")
    level = factory.Iterator(models.Deck.Level.values)
    is_custom = False
    created_by = factory.Maybe(
        "is_custom",
        yes_declaration=factory.SubFactory(UserFactory),
        no_declaration=None,
    )

    class Meta:
        model = models.Deck
