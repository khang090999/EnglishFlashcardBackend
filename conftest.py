"""Configuration file for pytest.

About session scope fixtures for Django models or db related fixtures:

- Plugin discussion: https://github.com/pytest-dev/pytest-django/issues/514

TLDR:
Session scope fixtures for Django models or db related fixtures are
discouraged due to potential issues with database transactions and
test isolation. Django model instances are mutable and can
lead to unintended side effects across tests if shared. For example,
in drf tests, on force_authenticate, the user instance is passed directly to
request.user which could lead to tests affecting each other
if they share the same user instance. Similar to force_login from
django test client, which update last_login field of user instance, which
sometimes cause errors when django tries to update in db but
it's already up to date.

"""

import collections.abc

from django.conf import settings
from django.core.files.storage import default_storage

import pytest


def pytest_configure() -> None:
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.

    """
    settings.DEBUG = False
    settings.RESTRICT_DEBUG_ACCESS = True
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/dev/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.MAILERS["default"]["BACKEND"] = (
        "django.core.mail.backends.console.EmailBackend"
    )

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # To separate test files from prod files
    settings.AWS_LOCATION = "test-files"



@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup) -> None:  # noqa: ANN001
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
def _enable_db_access_for_all_tests(django_db_setup, db) -> None:  # noqa: ANN001
    """Enable access to DB for all tests."""


@pytest.fixture(scope="session", autouse=True)
def _clean_up_test_files() -> collections.abc.Generator[None]:
    """Clear test files after finishing tests."""
    yield
    default_storage.bucket.objects.filter(
        Prefix=settings.AWS_LOCATION,
    ).delete()
