"""Extend default Django logging config.

- Removed `mail_admins` handler from `django`
  Since we use Sentry we don't need to send mails to the ADMINS

See default logging config for Django here:
https://docs.djangoproject.com/en/5.0/ref/logging/#default-logging-definition

"""

import copy

from django.utils.log import DEFAULT_LOGGING

logging_dict = copy.deepcopy(DEFAULT_LOGGING)
logging_dict["loggers"]["django"]["handlers"] = [
    "console",
]  # removed `mail_admins` here
LOGGING = logging_dict
