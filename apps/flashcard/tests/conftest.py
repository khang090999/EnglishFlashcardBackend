from types import ModuleType

from django.apps import apps
from django.contrib.auth import get_user_model

import pytest


@pytest.fixture
def card_models() -> ModuleType:
    """Load the registered flashcard models."""
    assert apps.is_installed("apps.flashcard")
    return apps.get_app_config("flashcard").models_module


@pytest.fixture
def learner(db):  # noqa: ANN001, ANN201
    """Create an account for learning records."""
    return get_user_model().objects.create(email="learner@example.test")


@pytest.fixture
def deck(card_models: ModuleType, db):  # noqa: ANN001, ANN201
    """Create a starter deck."""
    return card_models.Deck.objects.create(title="Basics", level="A1")


@pytest.fixture
def word(card_models: ModuleType, db):  # noqa: ANN001, ANN201
    """Create a vocabulary word."""
    return card_models.Word.objects.create(
        english="hello",
        vietnamese="xin chào",
    )
