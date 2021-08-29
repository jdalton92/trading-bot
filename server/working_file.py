import os

import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


def main():
    from alpaca_trade_api.entity import Asset as AlpacaAsset

    from assets.tasks import bulk_add_assets, update_assets, update_bars
    from core.alpaca import TradeApiRest
    from core.tasks import moving_average
    from users.models import User

    # asset_data = [
    #     AlpacaAsset(
    #         {
    #             "class": "us_equity",
    #             "easy_to_borrow": True,
    #             "exchange": "NASDAQ",
    #             "fractionable": True,
    #             "id": "8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
    #             "marginable": True,
    #             "name": "Tesla, Inc. Common Stock",
    #             "shortable": True,
    #             "status": "active",
    #             "symbol": "TSLA",
    #             "tradable": True,
    #         }
    #     ),
    # ]
    # superuser = User.objects.filter(is_superuser=True).first()
    # moving_average(superuser)
    # update_assets(asset_data)
    # update_bars(["MSFT"], "15Min", limit=2)
    api = TradeApiRest()
    asset = api.get_asset("TSLA")
    print("\nraw", asset.__dict__["_raw"])
    bulk_add_assets(asset.__dict__["_raw"])
    asset = api.get_asset("AAPL")
    bulk_add_assets(asset.__dict__["_raw"])
    print("\nraw", asset.__dict__["_raw"])


if __name__ == "__main__":
    main()
