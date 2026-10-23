from django.conf import settings
from django.urls import path

from health_check import views as health_check_views

from libs.health_checks import views

app_name = "libs.health_checks"

all_health_checks = [
    *settings.HEALTH_CHECK_MAIN_CHECKS,
    *settings.HEALTH_CHECK_CELERY_CHECKS,
]

# Django Health Check url
# See more details: https://codingjoe.dev/django-health-check/usage/
urlpatterns = [
    *(
        path(
            f"healthz/{name}/",
            health_check_views.HealthCheckView.as_view(
                checks=[check],
            ),
            name=f"healthz-{name}",
        )
        for (name, check) in all_health_checks
    ),
    path(
        "healthz/",
        health_check_views.HealthCheckView.as_view(
            checks=[check for _, check in all_health_checks],
        ),
        name="healthz",
    ),
    path(
        "livez/",
        views.liveness_check,
        name="livez",
    ),
    path(
        "readyz/",
        views.liveness_check,
        name="readyz",
    ),
]

if settings.DEBUG or settings.TESTING:
    urlpatterns += [
        path(
            "healthz/testing/",
            health_check_views.HealthCheckView.as_view(
                checks=[
                    check for _, check in settings.HEALTH_CHECK_MAIN_CHECKS
                ],
            ),
            name="healthz-testing",
        ),
    ]
