# Settings for custom health checks
HEALTH_CHECK_MAIN_CHECKS = [
    (
        "cache",
        "health_check.Cache",
    ),
    (
        "db",
        "health_check.Database",
    ),
    (
        "mail",
        "health_check.Mail",
    ),
    (
        "storage",
        "health_check.Storage",
    ),
]
HEALTH_CHECK_CELERY_CHECKS = [
    (
        "celery-ping",
        "health_check.contrib.celery.Ping",
    ),
]
