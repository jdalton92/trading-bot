import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
from server.orders.models import Order
from server.users.tests.factories import UserFactory

from .factories import OrderFactory


class OrderTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.asset = AssetFactory(
            symbol='TEST'
        )
        self.strategy = StrategyFactory(
            asset=self.asset
        )
        self.stop_loss = {
            "stop_price": 100.50,
            "limit_price": 110.30
        }
        self.take_profit = {
            "limit_price": 110.30
        }

    def test_create_order(self):
        """A order object can be created."""
        client_order_id = uuid.uuid4()
        order = Order(
            user=self.user,
            strategy=self.strategy,
            status=Order.OPEN,
            symbol=self.asset,
            quantity=100.05,
            side=Order.BUY,
            type=Order.MARKET,
            time_in_force=Order.DAY,
            client_order_id=client_order_id,
            limit_price=110.05,
            stop_price=90.05,
            trail_price=100.05,
            trail_percentage=50.05,
            extended_hours=True,
            order_class=Order.SIMPLE,
            take_profit=self.take_profit,
            stop_loss=self.stop_loss,
        )
        order.save()

        self.assertIn(order, Order.objects.all())
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.strategy, self.strategy)
        self.assertEqual(order.status, Order.OPEN)
        self.assertEqual(order.symbol.symbol, 'TEST')
        self.assertEqual(order.quantity, 100.05)
        self.assertEqual(order.side, Order.BUY)
        self.assertEqual(order.type, Order.MARKET)
        self.assertEqual(order.time_in_force, Order.DAY)
        self.assertEqual(str(order.client_order_id), str(client_order_id))
        self.assertEqual(order.limit_price, 110.05)
        self.assertEqual(order.stop_price, 90.05)
        self.assertEqual(order.trail_price, 100.05)
        self.assertEqual(order.trail_percentage, 50.05)
        self.assertTrue(order.extended_hours)
        self.assertEqual(order.order_class, Order.SIMPLE)
        self.assertEqual(order.take_profit, self.take_profit)
        self.assertEqual(order.stop_loss, self.stop_loss)

    def test_create_invalid_strategy_order(self):
        """A order symbol must be the same as the strategy asset symbol."""
        invalid_asset = AssetFactory()

        with self.assertRaisesRegex(
            ValidationError,
            'Strategy asset symbol and order symbol must be the same'
        ):
            OrderFactory(strategy=self.strategy, symbol=invalid_asset)
