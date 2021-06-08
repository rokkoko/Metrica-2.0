from .settings_base import *


ALLOWED_HOSTS = [
    'a-metrica.herokuapp.com',
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME_HEROKU'),
        'USER': os.getenv('DB_USER_HEROKU'),
        'PASSWORD': os.getenv('DB_PASSWORD_HEROKU'),
        'HOST': os.getenv('DB_HOST_HEROKU'),
        'PORT': '5432',
    }
}

INTERNAL_IPS = [
    'https://a-metrica.herokuapp.com/'
    ]

MIDDLEWARE.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE.append('django.middleware.cache.FetchFromCacheMiddleware')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'redis_cache': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'db_cache': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'table_cache'
        },
    'fs_cache': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'tmp/django_cache/')
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600
