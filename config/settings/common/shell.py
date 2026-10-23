from .installed_apps import LOCAL_APPS

# shell_plus configuration
# you can specify what additional libraries and blocks of
# code to be automatically imported when you run shell_plus
# command, in our case `inv django.shell`
# if you want factories to be included into your shell then you can do
# something like this
# *[("{}.factories".format(app), "*")
#   for app in LOCAL_APPS + TESTING_APPS]
# right inside SHELL_PLUS_PRE_IMPORTS

SHELL_PLUS = "ipython"
# what packages to preload inside shell plus
TOOLS_FOR_SHELL = [
    "from itertools import *",
    "from collections import *",
    "from datetime import *",
    "import arrow",
    "from django.db.models.functions import *",
    "from django.db.models.expressions import *",
]
TASKS_FOR_SHELL = [f"from {app}.tasks import *" for app in LOCAL_APPS]
SERVICES_FOR_SHELL = [f"from {app}.services import *" for app in LOCAL_APPS]
SHELL_PLUS_PRE_IMPORTS = (
    *TOOLS_FOR_SHELL,
    *SERVICES_FOR_SHELL,
    *TASKS_FOR_SHELL,
)

# Disable SQL Truncate
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
