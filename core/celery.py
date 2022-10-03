import os

from celery import Celery

from core.settings.base import SETTINGS_FILE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)

app = Celery("config", backend="redis", broker="redis://localhost:6379")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
