"""Views for healthcheck endpoints.

Disable atomic requests, because when `ATOMIC_REQUEST=True` django would
still go to db to check the state, meaning there would an error when db is
not available.

Note: these endpoints are still dependant on db, if you logged in via browser,
or in other words have session cookies.

"""

from django.db import transaction
from django.http import HttpResponse


@transaction.non_atomic_requests
def liveness_check(request) -> HttpResponse:
    """Check if app is alive."""
    return HttpResponse(status=204)
