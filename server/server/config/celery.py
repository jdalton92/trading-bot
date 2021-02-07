import os

import environ

from celery import Celery, shared_task

env = environ.Env()

# set the default Django settings module for the 'celery' program.
DJANGO_SETTINGS_MODULE = env("DJANGO_SETTINGS_MODULE")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)

app = Celery('server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
