import typing

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.core.notifications.email import DefaultEmailNotification

from apps.users.models import User


class UserPasswordResetEmailNotification(DefaultEmailNotification):
    """Used to send email with password reset link."""

    subject = _("Password Reset")
    template = "users/emails/password_reset.html"

    def __init__(self, user: User, **template_context) -> None:
        super().__init__(**template_context)
        self.user = user

    def get_recipient_list(self) -> list[str]:
        """Get email's recipients."""
        return [self.user.email]

    def get_template_context(self) -> dict[str, typing.Any]:
        """Get email's template context."""
        self.template_context.update(
            new_password_url=settings.FRONTEND_URL + settings.NEW_PASSWORD_URL,
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
        )
        return self.template_context
