import logging
import os

import celery.signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = celery.Celery("english-flashcards-backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

logger = logging.getLogger(__name__)


@celery.signals.worker_ready.connect
@celery.signals.beat_init.connect
def log_version(**kwargs) -> None:
    """Log the current version when the worker/beat is ready."""
    from libs import utils

    logger.info(
        "Running project version: %s(build: %s)",
        utils.get_latest_version("CHANGELOG.md"),
        utils.get_git_hash(),
    )
