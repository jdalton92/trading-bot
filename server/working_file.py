import os

import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


def main():
    from core.alpaca import TradeApiRest

    api = TradeApiRest()

    # account_info = api.account_info()
    # print("\n", account_info)
    # print("\nequity", account_info["equity"])

    last_quote = api.get_last_quote("TSLA")

    print("\n", last_quote)
    print("\nask_price", last_quote.__dict__["_raw"]["ask_price"])


if __name__ == "__main__":
    main()
