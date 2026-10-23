# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            # Specify timeout for a single statement. It helps to get
            # `OperationalError: canceling statement due to statement timeout`
            # when executing long-running SQL. This makes SQL query issues
            # easier to find, as HARAKIRI (see `uwsgi` config) can otherwise
            # kill regular HTTP requests without a readable traceback. For
            # expected long-running SQL (for example, data migrations for
            # large tables) use step like
            # migrations.RunSQL(
            #     "set local statement_timeout to '600s';",
            #     elidable=True,
            # ),
            "options": "-c statement_timeout=25s",
        },
    },
}
