from django.contrib.auth.models import AnonymousUser

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

import pytest

from apps.users.models import User

from ..permissions import IsAdmin, IsEditable


@pytest.mark.parametrize("method", ["get", "post", "put", "delete"])
@pytest.mark.parametrize(
    ["role", "is_staff", "is_superuser", "admin_allowed", "edit_allowed"],
    [
        ["student", False, False, False, False],
        ["teacher", False, False, False, True],
        ["admin", False, False, True, True],
        ["student", True, True, False, False],
        ["unknown", False, False, False, False],
    ],
)
def test_role_permissions(
    method: str,
    role: str,
    is_staff: bool,
    is_superuser: bool,
    admin_allowed: bool,
    edit_allowed: bool,
):
    """Require the appropriate role regardless of method or Django flags."""
    request = Request(getattr(APIRequestFactory(), method)("/"))
    request.user = User(
        role=role,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
    assert IsAdmin().has_permission(request, APIView()) is admin_allowed
    assert IsEditable().has_permission(request, APIView()) is edit_allowed


def test_anonymous_permissions():
    """Reject anonymous users without attempting to read their role."""
    request = Request(APIRequestFactory().get("/"))
    request.user = AnonymousUser()
    assert IsAdmin().has_permission(request, APIView()) is False
    assert IsEditable().has_permission(request, APIView()) is False
