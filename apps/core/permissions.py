from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.users.models import User


class IsAdmin(IsAuthenticated):
    """Allow authenticated users with the admin role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check authentication before checking the user's role."""
        return (
            super().has_permission(request, view)
            and request.user.role == User.Role.ADMIN
        )


class IsEditable(IsAuthenticated):
    """Allow authenticated users with the teacher or admin role."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Check authentication before checking the user's role."""
        return super().has_permission(request, view) and request.user.role in (
            User.Role.TEACHER,
            User.Role.ADMIN,
        )
