import http

from django.test.client import Client
from django.urls import reverse

import pytest
import pytest_lazy_fixtures

from apps.users.factories import UserFactory


@pytest.fixture(scope="module")
def unauthenticated_client() -> Client:
    """Return an unauthenticated client."""
    return Client()


@pytest.fixture(scope="module")
def staff_client() -> Client:
    """Return a client logged-in as staff."""
    staff_user = UserFactory(is_staff=True)
    client = Client()
    client.force_login(staff_user)
    return client


@pytest.fixture(scope="module")
def superuser_client() -> Client:
    """Return a client logged-in as superuser."""
    superuser = UserFactory(is_superuser=True)
    client = Client()
    client.force_login(superuser)
    return client


@pytest.mark.parametrize(
    argnames="client",
    argvalues=[
        pytest_lazy_fixtures.lf("unauthenticated_client"),
        pytest_lazy_fixtures.lf("staff_client"),
        pytest_lazy_fixtures.lf("superuser_client"),
    ],
)
def test_index_view(client: Client):
    """Ensure index page can be rendered."""
    index_view_url = reverse("index")
    response = client.get(index_view_url)
    assert response.status_code == http.HTTPStatus.OK
