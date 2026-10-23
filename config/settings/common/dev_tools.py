from django.http import HttpRequest

from .installed_apps import INSTALLED_APPS, LOCAL_APPS
from .middleware import MIDDLEWARE
from .shell import SHELL_PLUS_PRE_IMPORTS

INSTALLED_APPS += ("debug_toolbar",)

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)


def _show_toolbar_callback(request: HttpRequest) -> bool:
    """Only show debug toolbar for specific users (exclude testing).

    So you do not have to set `INTERNAL_IPS`. It's a little pain with docker.

    """
    from django.conf import settings

    from libs.permissions import can_access_debug_tools

    if settings.TESTING:
        return False
    return can_access_debug_tools(request.user)


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": _show_toolbar_callback,
}

FACTORIES_FOR_SHELL = [f"from {app}.factories import *" for app in LOCAL_APPS]
SHELL_PLUS_PRE_IMPORTS = (
    *SHELL_PLUS_PRE_IMPORTS,
    *FACTORIES_FOR_SHELL,
)
