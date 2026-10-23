# Application definition
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
    "knox",
    "drf_spectacular",
    "drf_standardized_errors",
)

THIRD_PARTY = (
    "storages",
    "django_extensions",
    "citext",
    "health_check",
)

LOCAL_APPS = (
    "apps.core",
    "apps.auth",
    "apps.users",
    "apps.flashcard",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + LOCAL_APPS
