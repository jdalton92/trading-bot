import os

import environ
from django.core.wsgi import get_wsgi_application

env = environ.Env()

DJANGO_SETTINGS_MODULE = env("DJANGO_SETTINGS_MODULE")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

application = get_wsgi_application()
