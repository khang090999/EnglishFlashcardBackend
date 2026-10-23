import django.urls

import rest_framework.response
import rest_framework.status
import rest_framework.test

import pytest
import pytest_lazy_fixtures

from apps.users.factories import DEFAULT_PASSWORD
from apps.users.models import User


@pytest.mark.parametrize(
    argnames="parametrize_user",
    argvalues=[
        None,
        pytest_lazy_fixtures.lf("user"),
        pytest_lazy_fixtures.lf("admin"),
    ],
)
def test_password_change(
    api_client: rest_framework.test.APIClient,
    parametrize_user: User | None,
):
    """Test that user can change password."""
    api_client.force_authenticate(user=parametrize_user)
    new_password = DEFAULT_PASSWORD + "?"
    response: rest_framework.response.Response = api_client.post(
        path=django.urls.reverse_lazy("api:v1:password-change"),
        data={
            "password": new_password,
            "password_confirm": new_password,
        },
    )
    if not parametrize_user:
        assert (
            response.status_code == rest_framework.status.HTTP_401_UNAUTHORIZED
        ), response.data
        return
    assert response.status_code == rest_framework.status.HTTP_200_OK, (
        response.data
    )
    api_client.force_authenticate(None)
    response: rest_framework.response.Response = api_client.post(
        django.urls.reverse_lazy("api:v1:login"),
        data={
            "email": parametrize_user.email,
            "password": new_password,
        },
    )
    assert response.status_code == rest_framework.status.HTTP_200_OK, (
        response.data
    )


@django.test.override_settings(
    # For tests we disable password validations, check pytest_configure
    AUTH_PASSWORD_VALIDATORS=[
        {
            "NAME": (
                "django.contrib.auth.password_validation."
                "CommonPasswordValidator"
            ),
        },
    ],
)
def test_password_change_validation(
    user_api_client: rest_framework.test.APIClient,
):
    """Test that in change password -> password validation works."""
    new_password = "password"  # noqa: S105
    response: rest_framework.response.Response = user_api_client.post(
        path=django.urls.reverse_lazy("api:v1:password-change"),
        data={
            "password": new_password,
            "password_confirm": new_password,
        },
    )
    assert (
        response.status_code == rest_framework.status.HTTP_400_BAD_REQUEST
    ), response.data
    assert (
        error := next(
            (
                error
                for error in response.data["errors"]
                if error["attr"] == "non_field_errors"
            ),
            None,
        )
    )
    assert error["detail"] == "This password is too common.", error


def test_password_change_match_validation(
    user_api_client: rest_framework.test.APIClient,
):
    """Test that in change password -> passwords must match."""
    response: rest_framework.response.Response = user_api_client.post(
        path=django.urls.reverse_lazy("api:v1:password-change"),
        data={
            "password": "1",
            "password_confirm": "2",
        },
    )
    assert (
        response.status_code == rest_framework.status.HTTP_400_BAD_REQUEST
    ), response.data
    assert (
        error := next(
            (
                error
                for error in response.data["errors"]
                if error["attr"] == "password_confirm"
            ),
            None,
        )
    )
    assert error["detail"] == "Passwords mismatch", error
