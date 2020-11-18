import json
import os

import django
import requests
from django.conf import settings  # NOQA

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.config.settings'
django.setup()


if __name__ == "__main__":
    import requests

    from api.assets.serializers import AssetBulkCreateSerializer
    from api.assets.tasks import update_asset_models
    from api.core.utils import TradeApiRest

    # update_asset_models()
    # api = TradeApiRest()
    # assets = api._list_assets()
    # assets = list(map(lambda asset: asset.__dict__['_raw'], assets[:3]))
    # with open('test_asset_data.json') as f:
    #     data = json.load(f)
    # serializer = AssetBulkCreateSerializer(data=data, many=True)
    # serializer.is_valid()
    # print('\n')
    # print('isValid', serializer.is_valid())
    # print('errors', serializer.errors)
    # print('data', serializer.data)
    # print('\n')
    # os.environ['NO_PROXY'] = '127.0.0.1'
    # headers = {
    #     "Authorization": "Token c35a9b6370ac4b0181f56902fbbe02bcf8e6ed67"
    # }
    # response = requests.post(
    #     'http://127.0.0.1:8000/v1/assets/bulkadd/',
    #     data=data,
    #     headers=headers
    # )
    # print('\n', response)
    # print('\n', response.content)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
