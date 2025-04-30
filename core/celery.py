import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks
app.autodiscover_tasks()
