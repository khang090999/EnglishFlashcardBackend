import pytest
import pytest_django

from .... import factories, models


@pytest.fixture(scope="module")
def instance(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.User:
    """Create instance for testing."""
    with django_db_blocker.unblock():
        return factories.UserFactory.create()


@pytest.fixture(scope="module")
def instance_batch(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> models.User:
    """Create instance for testing."""
    with django_db_blocker.unblock():
        return factories.UserFactory.create_batch(size=5)
