# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CACHES

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 1000,
            "SOCKET_CONNECT_TIMEOUT": 3,
            "SOCKET_TIMEOUT": 3,
            # https://redis.readthedocs.io/en/stable/connections.html#generic-client
            "REDIS_CLIENT_KWARGS": {
                "health_check_interval": 30,
            },
        },
        "KEY_PREFIX": "english_flashcards",
    },
}
