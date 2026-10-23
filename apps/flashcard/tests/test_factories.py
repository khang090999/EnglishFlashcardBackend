from django.db import models

import factory
import pytest

from .. import factories

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "model_factory",
    [
        factories.DeckFactory,
        factories.WordFactory,
        factories.DeckWordFactory,
        factories.BookmarkFactory,
        factories.WordProgressFactory,
        factories.UserLearningStateFactory,
    ],
)
def test_factory_creates_valid_model(
    model_factory: type[factory.django.DjangoModelFactory],
):
    """Every factory persists a valid model and its required relations."""
    instance = model_factory.create()
    instance.full_clean()
    assert instance.pk is not None
    for field in instance._meta.fields:
        if isinstance(field, models.ForeignKey):
            related = getattr(instance, field.name)
            if related is not None:
                related.full_clean()


def test_custom_deck_factory_creates_owner():
    """Custom decks automatically receive a valid creator."""
    deck = factories.DeckFactory(is_custom=True)
    deck.full_clean()
    assert deck.created_by_id is not None


def test_deck_word_batch_has_unique_positions():
    """Multiple memberships in one deck have distinct words and positions."""
    deck = factories.DeckFactory()
    memberships = factories.DeckWordFactory.create_batch(3, deck=deck)
    assert len({item.position for item in memberships}) == 3
    assert len({item.word_id for item in memberships}) == 3
    for membership in memberships:
        membership.full_clean()


def test_factory_build_does_not_persist_models():
    """Building a custom deck also builds its owner without database writes."""
    deck = factories.DeckFactory.build(is_custom=True)
    assert deck.pk is None
    assert deck.created_by.pk is None
