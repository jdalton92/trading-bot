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

        from assets.tests.factories import (
            AssetClassFactory,
            AssetFactory,
            ExchangeFactory,
        )
        from core.tests.factories import StrategyFactory
        from django.utils import timezone
        from users.models import User

        superuser = User.objects.filter(is_superuser=True).first()
        asset_class = AssetClassFactory(name="asset class")
        exchange = ExchangeFactory(name="exchange")
        asset_1 = AssetFactory(
            symbol="asset_1", asset_class=asset_class, exchange=exchange
        )
        asset_2 = AssetFactory(
            symbol="asset_2", asset_class=asset_class, exchange=exchange
        )

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
