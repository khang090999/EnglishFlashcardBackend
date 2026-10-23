"""API versioning urls.

When you need multiple API versions - consider using SpectacularAPIView
with preprocessing_hooks for splitting specs.
Or keep all APIs in the same spec for simplicity
(why not? depends on spec usage).
Or use custom generators.

"""

from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("v1/", include("config.urls.api.v1")),
]
