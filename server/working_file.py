import os

import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


def create_test_data():
    from datetime import timedelta

    from django.utils import timezone

    from assets.tests.factories import AssetClassFactory, AssetFactory, ExchangeFactory
    from core.tests.factories import StrategyFactory
    from users.models import User

    superuser = User.objects.get(pk=1)
    asset_class = AssetClassFactory(name="asset class")
    exchange = ExchangeFactory(name="exchange")
    asset_1 = AssetFactory(symbol="asset_1", asset_class=asset_class, exchange=exchange)
    asset_2 = AssetFactory(symbol="asset_2", asset_class=asset_class, exchange=exchange)

    StrategyFactory(
        user=superuser,
        asset=asset_1,
        start_date=timezone.now() - timedelta(days=1),
        end_date=timezone.now() + timedelta(days=10),
    )
    StrategyFactory(
        user=superuser,
        asset=asset_2,
        start_date=timezone.now() - timedelta(days=1),
        end_date=timezone.now() + timedelta(days=10),
    )


def main():
    from core.tasks import moving_average
    from users.models import User

    # superuser = User.objects.get(pk=1)
    print("\nusers", User.objects.all())
    # create_test_data()
    # moving_average(superuser)


if __name__ == "__main__":
    main()
