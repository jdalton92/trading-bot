import environ
from django.core.management.base import BaseCommand
from users.models import User

env = environ.Env()

SUPERUSER_FIRST_NAME = env("DJANGO_SUPERUSER_FIRSTNAME", default="Superuser")
SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default="superuser@tradingbot.com")
SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default="tradingbot123")
BAR_DATA = {
    "AAPL": [
        {
            "asset": "AAPL",
            "c": 121,
            "h": 126.4585,
            "l": 120.54,
            "o": 124.68,
            "t": 1614229200,
            "v": 134693926,
        },
        {
            "asset": "AAPL",
            "c": 121.2,
            "h": 124.85,
            "l": 121.2,
            "o": 122.59,
            "t": 1614315600,
            "v": 135693674,
        },
    ],
    "TSLA": [
        {
            "asset": "TSLA",
            "c": 682.6,
            "h": 737.2066,
            "l": 670.58,
            "o": 726.15,
            "t": 1614229200,
            "v": 36814146,
        },
        {
            "asset": "TSLA",
            "c": 671.01,
            "h": 706.7,
            "l": 659.51,
            "o": 700,
            "t": 1614315600,
            "v": 36281006,
        },
    ],
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-cs" "--create-superuser",
            action="store_true",
            help="Create a superuser account.",
            default=False,
        )

        parser.add_argument(
            "-gtd" "--generate-test-data",
            action="store_true",
            help="Create test data.",
            default=False,
        )

    def handle(self, *args, **kwargs):
        if kwargs["cs__create_superuser"]:
            if User.objects.filter(is_superuser=True).exists():
                self.stdout.write("Superuser already exists. Aborting...")
                return

            self.stdout.write("Creating superuser...")
            self.create_superuser()
            self.stdout.write("Done")

        if kwargs["gtd__generate_test_data"]:
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write("Superuser does not exist. Aborting...")
                return

            self.stdout.write("Creating test data...")
            self.create_test_data()
            self.stdout.write("Done")

    def create_superuser(self):
        User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD,
            first_name=SUPERUSER_FIRST_NAME,
        )

    def create_test_data(self):
        from datetime import timedelta

        from assets.models import AssetClass, Exchange
        from assets.serializers import BarSerializer
        from assets.tests.factories import AssetFactory
        from core.tests.factories import StrategyFactory
        from django.db.utils import IntegrityError
        from django.utils import timezone
        from users.models import User

        superuser = User.objects.filter(is_superuser=True).first()
        asset_class, _ = AssetClass.objects.get_or_create(
            name="us_equity", is_active=True
        )
        exchange, _ = Exchange.objects.get_or_create(name="NASDAQ", is_active=True)
        asset_1 = AssetFactory(
            symbol="TSLA", asset_class=asset_class, exchange=exchange
        )
        asset_2 = AssetFactory(
            symbol="MSFT", asset_class=asset_class, exchange=exchange
        )

        StrategyFactory(
            user=superuser,
            asset=asset_1,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=10),
            trade_value=100,
        )
        StrategyFactory(
            user=superuser,
            asset=asset_2,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=10),
            trade_value=100,
        )

        for asset_symbol in BAR_DATA:
            for bar in BAR_DATA[asset_symbol]:
                bar = bar.__dict__["_raw"]
                bar["asset"] = asset_symbol
                serializer = BarSerializer(data=bar)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError:
                        # Fail silently when data already exists
                        pass
