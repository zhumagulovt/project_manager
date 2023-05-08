import os

from celery import Celery

from .settings import base as settings

if settings.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.production"
    )

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
