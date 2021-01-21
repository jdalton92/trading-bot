import json
import os

import django
import requests
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'
django.setup()


def get_bars(symbols, timeframe, limit=None, start=None, end=None,
             after=None, until=None):
    """Fetch bar data for list of symbols."""
    if not isinstance(symbols, list):
        symbols = [symbols]
    api = TradeApiRest()
    bars = api._get_bars(
        symbols, timeframe, limit, start, end, after, until
    )

    # for asset in bars:
    #     for bar in asset:
    #         # TO DO - TRANSFORM ALPACABAR INSTANCE TO BAR MODEL FORMAT
    #         serializer = BarSerializer(data=bar)
    #         # Fail silently for bulk add
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()

    return bars


if __name__ == "__main__":

    from server.assets.models import Asset
    from server.assets.serializers import BarSerializer
    from server.core.alpaca import TradeApiRest

    symbols = ["TSLA", "AAPL"]
    bars = get_bars(symbols, '1D', 10)
    print('bars', bars['AAPL'][0].__dict__['raw'])
