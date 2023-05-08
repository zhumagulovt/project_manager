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

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_FROM = env.str("EMAIL_HOST_USER")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.str("EMAIL_HOST_PORT")
EMAIL_USE_TLS = True
