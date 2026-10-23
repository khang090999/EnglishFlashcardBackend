# Rest framework API configuration
from datetime import timedelta

from libs.utils import get_latest_version

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "knox.auth.TokenAuthentication",
        # SessionAuthentication is also used for CSRF
        # validation on ajax calls from the frontend
        "rest_framework.authentication.SessionAuthentication",
    ),
    # `BaseViewSet` must be used in order to define new viewsets.
    # This viewset is inherited from `ActionPermissionsMixin` which can be used
    # to define all necessary permissions.
    # In order to be secure, all permissions are disabled by default
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAdminUser",),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "libs.api.renderers.CustomBrowsableAPIRenderer",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "libs.api.filter_backends.CustomDjangoFilterBackend",
        "libs.open_api.filters.OrderingFilterBackend",
        "libs.open_api.filters.SearchFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "libs.api.pagination.CustomLimitOffsetPagination"
    ),
    "PAGE_SIZE": 25,
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Limit max objects in list APIs
MAX_PAGINATION_SIZE = 100

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "English Flashcards Api",
    "DESCRIPTION": "Api for English Flashcards",
    "VERSION": get_latest_version("CHANGELOG.md"),
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    "POSTPROCESSING_HOOKS": [
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums",
    ],
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": [
        "libs.permissions.HasAccessToDebugTools",
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "docExpansion": "none",
    },
}

# https://jazzband.github.io/django-rest-knox/settings/
REST_KNOX = {
    "SECURE_HASH_ALGORITHM": "hashlib.sha512",
    "AUTH_TOKEN_CHARACTER_LENGTH": 64,
    "TOKEN_TTL": timedelta(weeks=2),
    "TOKEN_LIMIT_PER_USER": None,
    "AUTO_REFRESH": False,
    "USER_SERIALIZER": "apps.users.api.serializers.UserSerializer",
}
