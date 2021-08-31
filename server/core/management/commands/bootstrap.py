import environ
from django.core.management.base import BaseCommand
from users.models import User

env = environ.Env()

SUPERUSER_FIRST_NAME = env("DJANGO_SUPERUSER_FIRSTNAME", default="Superuser")
SUPERUSER_EMAIL = env("DJANGO_SUPERUSER_EMAIL", default="superuser@tradingbot.com")
SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD", default="tradingbot123")


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
        import json
        from datetime import timedelta

        from assets.models import Asset, AssetClass, Bar, Exchange
        from core.models import Strategy
        from django.utils import timezone
        from users.models import User

        superuser = User.objects.filter(is_superuser=True).first()

        asset_class, _ = AssetClass.objects.get_or_create(
            name="us_equity", is_active=True
        )
        exchange, _ = Exchange.objects.get_or_create(name="NASDAQ", is_active=True)

        asset_tsla, _ = Asset.objects.get_or_create(
            id="8ccae427-5dd0-45b3-b5fe-7ba5e422c766",
            symbol="TSLA",
            asset_class=asset_class,
            exchange=exchange,
            status=Asset.ACTIVE,
            tradable=True,
            shortable=True,
            marginable=True,
            easy_to_borrow=True,
        )

        Strategy.objects.update_or_create(
            user=superuser,
            asset=asset_tsla,
            type=Strategy.MOVING_AVERAGE_7D,
            trade_value=100,
            defaults={
                "start_date": timezone.now() - timedelta(days=1),
                "end_date": timezone.now() + timedelta(days=10),
            },
        )

        with open("assets/tests/sample_tsla_bars.json") as f:
            tsla = Asset.objects.get(symbol="TSLA")
            bars = json.load(f)
            objs = [
                Bar(
                    asset=tsla,
                    t=bar["t"],
                    o=bar["o"],
                    h=bar["h"],
                    l=bar["l"],
                    c=bar["c"],
                    v=bar["v"],
                )
                for bar in bars
            ]
            Bar.objects.bulk_create(objs, batch_size=1000, ignore_conflicts=True)
