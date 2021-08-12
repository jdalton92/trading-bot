import json
import os

import django
import requests
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "server.config.settings"
django.setup()


def get_bars(
    symbols, timeframe, limit=None, start=None, end=None, after=None, until=None
):
    """Fetch bar data for list of symbols."""
    if not isinstance(symbols, list):
        symbols = [symbols]
    api = TradeApiRest()
    bars = api.get_bars(symbols, timeframe, limit, start, end, after, until)

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

    api = TradeApiRest()
    # order = api.submit_order(
    #     symbol="TSLA",
    #     qty=1,
    #     side="buy",
    #     type="market",
    #     time_in_force="ioc"
    # )
    orders = api.get_order_by_client_order_id("a39ee42d-bb23-4395-8049-b8e69a1efd81")
    print(orders)

    sample_order = {
        "asset_class": "us_equity",
        "asset_id": "8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
        "canceled_at": None,
        "client_order_id": "a39ee42d-bb23-4395-8049-b8e69a1efd81",
        "created_at": "2021-01-27T04:41:51.452242Z",
        "expired_at": None,
        "extended_hours": False,
        "failed_at": "2021-01-27T04:41:51.46134Z",
        "filled_at": None,
        "filled_avg_price": None,
        "filled_qty": "0",
        "hwm": None,
        "id": "25391b18-c94b-4b54-ae79-f407e36f980a",
        "legs": None,
        "limit_price": None,
        "order_class": "",
        "order_type": "market",
        "qty": "1",
        "replaced_at": None,
        "replaced_by": None,
        "replaces": None,
        "side": "buy",
        "status": "rejected",
        "stop_price": None,
        "submitted_at": "2021-01-27T04:41:51.444456Z",
        "symbol": "TSLA",
        "time_in_force": "ioc",
        "trail_percent": None,
        "trail_price": None,
        "type": "market",
        "updated_at": "2021-01-27T04:41:51.47071Z",
    }
