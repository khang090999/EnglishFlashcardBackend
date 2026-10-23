from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthAppConfig(AppConfig):
    """Default configuration for Auth app."""

    name = "apps.auth"
    verbose_name = _("Auth")
    label = "authentication"

    def ready(self) -> None:
        from .api import schema  # noqa
