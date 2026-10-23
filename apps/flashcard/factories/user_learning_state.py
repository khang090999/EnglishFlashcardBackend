import factory

from apps.users.factories import UserFactory

from .. import models
from .deck import DeckFactory


class UserLearningStateFactory(
    factory.django.DjangoModelFactory[models.UserLearningState],
):
    """Generate a learner's last opened deck pointer."""

    user = factory.SubFactory(UserFactory)
    last_deck = factory.SubFactory(DeckFactory)

    class Meta:
        model = models.UserLearningState
