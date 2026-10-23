import socket

import decouple

from .config import *

DATABASES["default"].update(
    # `runserver` can't be used with persistent connections, see
    # https://docs.djangoproject.com/en/dev/ref/databases/#caveats
    CONN_MAX_AGE=0,
)

INTERNAL_IPS = (
    "0.0.0.0",  # noqa: S104
    "127.0.0.1",
)
# Hack to have working `debug` context processor when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += (ip[:-1] + "1",)

# if this option is True - celery task will run like default functions,
# not asynchronous
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = decouple.config(
    "celery_task_always_eager",
    default=False,
    cast=bool,
)

# Allow access to debug features
RESTRICT_DEBUG_ACCESS = False

# Disable password validators
AUTH_PASSWORD_VALIDATORS = []

MIDDLEWARE += ("corsheaders.middleware.CorsMiddleware",)

INSTALLED_APPS += (
    "django_probes",  # wait for DB to be ready to accept connections
    "corsheaders",  # provide CORS for local development
)
# Provide CORS for local development
# This is necessary when developer wants to run the frontend application
# locally and communicate with the local backend server. This does not affect
# django applications with their own frontend or mobile APIs
# see doc here
# https://github.com/ottoyiu/django-cors-headers/

CORS_ORIGIN_ALLOW_ALL = True
# Custom headers
CORS_EXPOSE_HEADERS = ()
CORS_ALLOW_HEADERS = (
    "x-requested-with",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-csrftoken",
    "user-agent",
    "accept-encoding",
    # Sentry headers
    "baggage",
    "sentry-trace",
)

# S3 config
AWS_S3_ENDPOINT_URL = "http://s3.rustfs.localhost:9000"
AWS_S3_ACCESS_KEY_ID = decouple.config("aws_s3_access_key_id")
AWS_S3_SECRET_ACCESS_KEY = decouple.config("aws_s3_secret_access_key")

STORAGE_UI = AWS_S3_ENDPOINT_URL.replace("9000", "9001")
