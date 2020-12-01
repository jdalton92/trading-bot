import json
import os

import django
import requests
from django.conf import settings  # NOQA

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'
django.setup()


if __name__ == "__main__":

    from server.assets.models import Asset
    from server.assets.serializers import AssetSerializer
    from server.assets.tasks import update_assets
    from server.core.utils import TradeApiRest

    update_assets()
