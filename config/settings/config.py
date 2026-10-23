import sys

import decouple
from dj_database_url import parse as db_url

from .common import *

DEBUG = decouple.config("app_debug", default=False, cast=bool)

# Enable restriction to access debug tools like swagger, django debug toolbars,
# Admin page for non-local envs
RESTRICT_DEBUG_ACCESS = True

ENVIRONMENT = decouple.config("environment")

FRONTEND_URL = decouple.config("frontend_url", default="")

DATABASES["default"].update(decouple.config("database_url", cast=db_url))

AWS_STORAGE_BUCKET_NAME = decouple.config("aws_s3_bucket_name")
AWS_S3_REGION_NAME = decouple.config("aws_s3_direct_region")
AWS_S3_ENDPOINT_URL = f"https://s3.{AWS_S3_REGION_NAME}.amazonaws.com"

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": decouple.config("email_host"),
            "username": decouple.config("email_host_user"),
            "password": decouple.config("email_host_password"),
            "port": decouple.config("email_host_port", cast=int),
            "use_tls": decouple.config("email_host_use_tls", cast=bool),
        },
    },
}
EMAIL_UI_URL = decouple.config("email_ui_url")
DEFAULT_FROM_EMAIL = (
    decouple.config("default_from_email") or "no-reply@english-flashcards.com"
)

redis_url = decouple.config("redis_url")

CELERY_TASK_DEFAULT_QUEUE = (
    f"{APP_LABEL.lower().replace(' ', '-')}-{ENVIRONMENT}"
)
CELERY_BROKER_URL = redis_url
CELERY_RESULT_BACKEND = redis_url

CACHES["default"].update(
    LOCATION=redis_url,
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = decouple.config("django_secret_key")
ALLOWED_HOSTS = ["*"]

# disable django DEBUG if we run celery worker
if "celery" in sys.argv[0]:
    DEBUG = False

if DEBUG:
    # Dev tools settings
    from .common.dev_tools import *
