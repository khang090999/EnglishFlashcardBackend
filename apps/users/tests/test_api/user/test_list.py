from django.urls import reverse_lazy

from rest_framework import status, test
from rest_framework.response import Response

import pytest
import pytest_lazy_fixtures

from .... import models


@pytest.mark.parametrize(
    argnames=[
        "parametrize_user",
        "status_code",
    ],
    argvalues=[
        [
            None,
            status.HTTP_401_UNAUTHORIZED,
        ],
        [
            pytest_lazy_fixtures.lf("user"),
            status.HTTP_403_FORBIDDEN,
        ],
        [
            pytest_lazy_fixtures.lf("admin"),
            status.HTTP_200_OK,
        ],
    ],
)
@pytest.mark.usefixtures("instance_batch")
def test_api(
    api_client: test.APIClient,
    parametrize_user: models.User | None,
    status_code: int,
):
    """Test that admins can list all instances."""
    api_client.force_authenticate(user=parametrize_user)
    response: Response = api_client.get(
        path=reverse_lazy("api:v1:users-list"),
    )
    assert response.status_code == status_code, response.data
