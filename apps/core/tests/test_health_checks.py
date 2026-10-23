from django.urls import reverse_lazy

from rest_framework import status, test


def test_liveness_check(api_client: test.APIClient):
    """Test liveness check."""
    response = api_client.get(reverse_lazy("healthz:livez"))
    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        response.content.decode("UTF-8")
    )  # type: ignore


def test_ready_check(api_client: test.APIClient):
    """Test ready check."""
    response = api_client.get(reverse_lazy("healthz:readyz"))
    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        response.content.decode("UTF-8")
    )  # type: ignore


def test_health_check(api_client: test.APIClient):
    """Test health check."""
    response = api_client.get(reverse_lazy("healthz:healthz-testing"))
    assert response.status_code == status.HTTP_200_OK, response.content.decode(
        "UTF-8",
    )  # type: ignore
