import os

import django
from django.conf import settings  # NOQA

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.config.settings'
django.setup()


if __name__ == "__main__":
    from api.assets.tasks import update_asset_models

    update_asset_models()
