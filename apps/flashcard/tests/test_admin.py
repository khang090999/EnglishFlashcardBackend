from types import ModuleType

from django.contrib import admin
from django.test import Client, RequestFactory
from django.urls import reverse

import pytest

from apps.users.models import User

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "model_name",
    [
        "Deck",
        "Word",
        "DeckWord",
        "Bookmark",
        "WordProgress",
        "UserLearningState",
    ],
)
def test_admin_pages_render(
    card_models: ModuleType,
    client: Client,
    learner: User,
    model_name: str,
):
    """Every model exposes working list and add screens for staff."""
    learner.is_staff = True
    learner.is_superuser = True
    learner.save()
    client.force_login(learner)
    model = getattr(card_models, model_name)
    assert admin.site.is_registered(model)
    for page in ("changelist", "add"):
        url = reverse(f"admin:flashcard_{model_name.lower()}_{page}")
        assert client.get(url).status_code == 200


def test_admin_validates_creator(
    card_models: ModuleType,
    rf: RequestFactory,
    learner: User,
):
    """Invalid custom decks report a creator form error."""
    request = rf.get("/admin/")
    request.user = learner
    form_class = admin.site.get_model_admin(card_models.Deck).get_form(request)
    form = form_class(
        data={"title": "Custom", "level": "A1", "is_custom": True},
    )
    assert not form.is_valid()
    assert "created_by" in form.errors
