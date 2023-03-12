from .base import *  # noqa
from .base import env

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# django-cors-headers
# ------------------------------------------------------------------------------
# https://github.com/adamchainz/django-cors-headers#setup
INSTALLED_APPS += ["corsheaders"]  # noqa F405 type: ignore

MIDDLEWARE += ["corsheaders.middleware.CorsMiddleware"]  # noqa F405

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
