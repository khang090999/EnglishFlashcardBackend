import re

from django.conf import settings
from django.core import mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status, test
from rest_framework.response import Response

from apps.users.factories import DEFAULT_PASSWORD
from apps.users.models import User

from ... import notifications, services


def _get_reset_token_from_email(user_email: str) -> tuple[str, str] | None:
    """Extract reset token from email."""
    subject = (
        f"{settings.APP_LABEL} - "
        f"{notifications.UserPasswordResetEmailNotification.subject}"
    )
    reset_email = next(
        (
            email
            for email in mail.outbox
            if email.subject == subject and email.to == [user_email]
        ),
        None,
    )
    if not reset_email:
        return None
    token_matches = re.findall(
        pattern=r"(?=token=(.*)\")",
        string=reset_email.alternatives[0][0],
    )
    uid, *token_parts = token_matches[0].split("-")
    return uid, "-".join(token_parts)


def test_password_reset(
    user_api_client: test.APIClient,
    user: User,
):
    """Test that user can request password reset and it will send an email."""
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:password-reset"),
        data={
            "email": user.email,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    # Check that email was sent and contains needed token
    assert _get_reset_token_from_email(user_email=user.email)


def test_password_reset_non_existent_email(
    api_client: test.APIClient,
):
    """Test that if user uses email of unknown user, email will not be sent."""
    response: Response = api_client.post(
        path=reverse_lazy("api:v1:password-reset"),
        data={
            "email": "local@localhost",
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    # Check that email wasn't sent
    assert not _get_reset_token_from_email(user_email="local@localhost")


def test_password_reset_confirm(
    user_api_client: test.APIClient,
    user: User,
):
    """Test that user can change password with token."""
    services.reset_user_password(user=user)
    uid_and_token = _get_reset_token_from_email(user_email=user.email)
    assert uid_and_token
    uid, token = uid_and_token
    new_password = DEFAULT_PASSWORD + "?"
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    # Check that password was indeed changed
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:login"),
        data={
            "email": user.email,
            "password": DEFAULT_PASSWORD,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:login"),
        data={
            "email": user.email,
            "password": new_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data


def test_password_reset_confirm_mismatch_passwords(
    api_client: test.APIClient,
    user: User,
):
    """Test that user needs to match `password_confirm` with `password`."""
    services.reset_user_password(user=user)
    uid_and_token = _get_reset_token_from_email(user_email=user.email)
    assert uid_and_token
    uid, token = uid_and_token
    response: Response = api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": DEFAULT_PASSWORD,
            "password_confirm": DEFAULT_PASSWORD + "?",
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert response.data["errors"][0]["detail"] == "Passwords mismatch", (
        response.data
    )


def test_password_reset_confirm_user_not_found(
    api_client: test.APIClient,
    user: User,
):
    """Test case when user can't be found from uid."""
    services.reset_user_password(user=user)
    uid_and_token = _get_reset_token_from_email(user_email=user.email)
    assert uid_and_token
    _, token = uid_and_token
    new_password = DEFAULT_PASSWORD + "?"
    response: Response = api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": urlsafe_base64_encode(force_bytes(-1)),
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert response.data["errors"][0]["detail"] == "Invalid uid", response.data


def test_password_reset_confirm_reuse(
    user_api_client: test.APIClient,
    user: User,
):
    """Test that user can't reuse token for password change."""
    services.reset_user_password(user=user)
    uid_and_token = _get_reset_token_from_email(user_email=user.email)
    assert uid_and_token
    uid, token = uid_and_token
    new_password = DEFAULT_PASSWORD + "?"
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": new_password,
            "password_confirm": new_password,
            "uid": uid,
            "token": token,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert response.data["errors"][0]["detail"] == "Invalid token", (
        response.data
    )


def test_password_reset_confirm_token_validation(
    user_api_client: test.APIClient,
    user: User,
):
    """Test validation against invalid uid."""
    response: Response = user_api_client.post(
        path=reverse_lazy("api:v1:password-reset-confirm"),
        data={
            "password": "password",
            "password_confirm": "password",
            "uid": "uid",
            "token": "token",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert response.data["errors"][0]["detail"] == "Invalid uid", response.data
