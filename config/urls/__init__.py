from django.contrib import admin
from django.urls import include, path

from apps.core.views import IndexView

from .debug import urlpatterns as debug_urlpatterns

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mission-control-center/", admin.site.urls),
    path("", include("libs.health_checks.urls", namespace="healthz")),
    path("auth/", include("rest_framework.urls")),
    path("api/", include("config.urls.api")),
]
urlpatterns += debug_urlpatterns
