import uuid
from decimal import Decimal

from django.test import TestCase
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order, StopLoss, TakeProfit

from .factories import OrderFactory, StopLossFactory, TakeProfitFactory


class StopLossTests(TestCase):

    def test_create_stop_loss(self):
        """Stop loss object can be created."""
        stop_loss = StopLoss(
            stop_price=100.50,
            limit_price=110.30
        )
        stop_loss.save()

        self.assertIn(stop_loss, StopLoss.objects.all())
        self.assertEqual(stop_loss.stop_price, Decimal(100.50))
        self.assertEqual(stop_loss.limit_price, Decimal(110.30))


class TakeProfitTests(TestCase):

    def test_create_take_profit(self):
        """Take profit object can be created."""
        take_profit = TakeProfit(
            limit_price=110.30
        )
        take_profit.save()

        self.assertIn(take_profit, TakeProfit.objects.all())
        self.assertEqual(take_profit.limit_price, Decimal(110.30))


class OrderTests(TestCase):

    def setUp(self):
        self.asset = AssetFactory(
            symbol='TEST'
        )
        self.stop_loss = StopLossFactory(
            stop_price=100.50,
            limit_price=110.30
        )
        self.take_profit = TakeProfitFactory(
            limit_price=110.30
        )

    def test_create_order(self):
        """A order object can be created."""
        client_order_id = uuid.uuid4()
        order = Order(
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
        self.assertEqual(order.take_profit.pk, self.take_profit.pk)
        self.assertEqual(order.stop_loss.pk, self.stop_loss.pk)
