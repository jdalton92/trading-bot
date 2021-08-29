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
            "-ctd" "--create-test-data",
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

        if kwargs["ctd__create_test_data"]:
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

        from assets.models import Asset, AssetClass, Exchange
        from assets.serializers import BarSerializer
        from core.models import Strategy
        from django.db.utils import IntegrityError
        from django.utils import timezone
        from users.models import User

        superuser = User.objects.filter(is_superuser=True).first()

        asset_class, _ = AssetClass.objects.get_or_create(
            name="us_equity", is_active=True
        )
        exchange, _ = Exchange.objects.get_or_create(name="NASDAQ", is_active=True)

        asset_1, _ = Asset.objects.get_or_create(
            id="8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
            symbol="TSLA",
            asset_class=asset_class,
            exchange=exchange,
            status=Asset.ACTIVE,
            tradable=True,
            shortable=True,
            marginable=True,
            easy_to_borrow=True

        )
        asset_2, _ = Asset.objects.get_or_create(
            id="b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            symbol="AAPL",
            asset_class=asset_class,
            exchange=exchange,
            status=Asset.ACTIVE,
            tradable=True,
            shortable=True,
            marginable=True,
            easy_to_borrow=True
        )

        Strategy.objects.get_or_create(
            user=superuser,
            asset=asset_1,
            type=Strategy.MOVING_AVERAGE_7D,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=10),
            trade_value=100,
        )
        Strategy.objects.get_or_create(
            user=superuser,
            asset=asset_2,
            type=Strategy.MOVING_AVERAGE_7D,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=10),
            trade_value=100,
        )

        for asset_symbol in BAR_DATA:
            for bar in BAR_DATA[asset_symbol]:
                bar["asset"] = asset_symbol
                serializer = BarSerializer(data=bar)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError:
                        # Fail silently when data already exists
                        pass
