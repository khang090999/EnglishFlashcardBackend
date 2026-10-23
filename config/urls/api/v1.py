from django.conf import settings
from django.urls import include, path

app_name = "v1"

urlpatterns = [
    path("auth/", include("apps.auth.api.urls")),
    path("users/", include("apps.users.api.urls")),
]

# Add open_api urls only to not production envs
if settings.DEBUG:
    urlpatterns.append(
        path(
            "open-api/",
            include("config.urls.open_api", namespace="open-api"),
        ),
    )
