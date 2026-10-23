import dataclasses
import platform

import django
from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import TemplateView

from libs import (
    permissions as libs_permissions,
    utils as libs_utils,
)


@dataclasses.dataclass
class Changelog:
    """Class keeping changelog data."""

    name: str
    text: str
    version: str
    swagger_api_ui: str | None
    redoc_api_ui: str | None


class AppStatsMixin:
    """Add information about app to context."""

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        storage_ui_url = getattr(settings, "STORAGE_UI", None)
        context.update(
            show_debug_tools=libs_permissions.can_access_debug_tools(
                self.request.user,
            ),
            env=settings.ENVIRONMENT,
            version=libs_utils.get_latest_version("CHANGELOG.md"),
            git_hash=libs_utils.get_git_hash(),
            python_version=platform.python_version(),
            django_version=django.get_version(),
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
            email_ui_url=settings.EMAIL_UI_URL,
            storage_ui_url=storage_ui_url,
        )
        return context


class IndexView(AppStatsMixin, TemplateView):
    """Class-based view for that shows version of open_api file on main page.

    Displays the current version of the open_api specification and changelog.

    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Load changelog data from files."""
        context = super().get_context_data(**kwargs)
        open_api_ui_urls = {
            "swagger_api_ui": "api:v1:open-api:swagger",
            "redoc_api_ui": "api:v1:open-api:redoc",
        }

        for open_api_type, open_api_view_name in open_api_ui_urls.items():
            try:
                url = reverse(open_api_view_name)
            except NoReverseMatch:
                url = None
            open_api_ui_urls[open_api_type] = url

        context["changelog"] = Changelog(
            name=settings.SPECTACULAR_SETTINGS.get("TITLE"),
            text=libs_utils.get_changelog_html("CHANGELOG.md"),
            version=settings.SPECTACULAR_SETTINGS.get("VERSION"),
            **open_api_ui_urls,
        )
        return context
