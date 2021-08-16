from datetime import timedelta

from assets.tests.factories import AssetFactory
from core.models import Strategy
from django.test import TestCase
from django.utils import timezone
from orders.tests.factories import OrderFactory
from users.tests.factories import UserFactory

from .factories import StrategyFactory


class StrategyTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.asset = AssetFactory()

    def test_create_strategy(self):
        """Strategy object can be created."""
        time_now = timezone.now()
        strategy = Strategy(
            user=self.user,
            type=Strategy.MOVING_AVERAGE_14D,
            asset=self.asset,
            start_date=time_now - timedelta(days=2),
            end_date=time_now + timedelta(days=2),
            trade_value=10000,
        )
        strategy.save()

        self.assertIn(strategy, Strategy.objects.all())
        self.assertEqual(strategy.user, self.user)
        self.assertEqual(strategy.type, "moving_average_14d")
        self.assertEqual(str(strategy.asset.pk), self.asset.pk)
        self.assertEqual(strategy.start_date, time_now - timedelta(days=2))
        self.assertEqual(strategy.end_date, time_now + timedelta(days=2))
        self.assertEqual(strategy.trade_value, 10000)

    def test_add_orders_to_strategy(self):
        """Strategy object can have orders associated."""
        strategy = StrategyFactory(
            user=self.user,
            asset=self.asset,
        )
        order = OrderFactory(user=self.user, asset_id=self.asset, strategy=strategy)

        self.assertTrue(strategy.orders.filter(pk=order.pk).exists())
