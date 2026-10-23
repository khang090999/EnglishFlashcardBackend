import factory

from .. import models


class WordFactory(factory.django.DjangoModelFactory[models.Word]):
    """Generate placeholders; override text for real translations."""

    english = factory.Sequence(lambda number: f"word {number}")
    vietnamese = factory.Sequence(lambda number: f"từ {number}")
    example = factory.Faker("sentence")

    class Meta:
        model = models.Word
