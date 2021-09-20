import os

import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


def main():
    from core.alpaca import TradeApiRest

    api = TradeApiRest()

    response = api.list_position_by_symbol("TSLA")

    print("\n", response)
    print("\ndir", dir(response))


if __name__ == "__main__":
    main()
