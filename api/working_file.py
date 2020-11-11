import json
import os

import django
from django.conf import settings  # NOQA

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.config.settings'
django.setup()


if __name__ == "__main__":
    from api.assets.serializers import AssetBulkCreateSerializer
    from api.assets.tasks import update_asset_models
    from api.core.utils import TradeApiRest

    # update_asset_models()
    # api = TradeApiRest()
    # assets = api._list_assets()
    # assets = list(map(lambda asset: asset.__dict__['_raw'], assets[:3]))

    serializer = AssetBulkCreateSerializer(data=data, many=True)
    serializer.is_valid()
    print('\n')
    print('isValid', serializer.is_valid())
    print('errors', serializer.errors)
    print('data', serializer.data)
    print('\n')
    serializer.save()
