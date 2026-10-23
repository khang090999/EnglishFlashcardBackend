from rest_framework import test

import pytest

from apps.users import (
    factories as users_factories,
    models as users_models,
)


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture
def user() -> users_models.User:
    """Create default user."""
    return users_factories.UserFactory.create()


@pytest.fixture
def user_api_client(
    api_client: test.APIClient,
    user: users_models.User,
) -> test.APIClient:
    """Create api client."""
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture
def admin() -> users_models.User:
    """Create admin user."""
    return users_factories.AdminUserFactory.create()
