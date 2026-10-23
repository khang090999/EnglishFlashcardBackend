from .authentication import *
from .business_logic import *
from .cache import *
from .celery import *
from .databases import *
from .drf import *
from .health_check import *
from .installed_apps import *
from .internationalization import *
from .logging import *
from .middleware import *
from .paths import *
from .sentry import *
from .shell import *
from .storage import *
from .templates import *

APPEND_SLASH = False
ALLOWED_HOSTS = ["*"]
SITE_ID = 1
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TESTING = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Custom settings
APP_LABEL = "English Flashcards"

# a password URL for a frontend page; sent in a reset email
NEW_PASSWORD_URL = "TODO"  # noqa: S105
