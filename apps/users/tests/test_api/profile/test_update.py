from django.urls import reverse_lazy

from rest_framework import status, test
from rest_framework.response import Response

import pytest
import pytest_lazy_fixtures

from .... import models
from ....api import serializers


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
            status.HTTP_200_OK,
        ],
    ],
)
def test_api(
    api_client: test.APIClient,
    parametrize_user: models.User | None,
    status_code: int,
):
    """Test update."""
    api_client.force_authenticate(user=parametrize_user)
    data = serializers.UserSerializer(
        instance=parametrize_user or models.User(),
    ).data
    # Update it when api will be ready for s3 integration
    data["avatar"] = None
    response: Response = api_client.put(
        path=reverse_lazy("api:v1:profile"),
        data=data,
    )
    assert response.status_code == status_code, response.data
