import uuid
from decimal import Decimal

from django.test import TestCase
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order, StopLoss, TakeProfit

from .factories import OrderFactory


class StopLossTests(TestCase):

    def test_create_stop_loss(self):
        """Stop loss object can be created."""
        stop_loss = StopLoss(
            stop_price=Decimal(100.50),
            limit_price=Decimal(110.30),
        )
        stop_loss.save()

        self.assertIn(stop_loss, StopLoss.objects.all())
        self.assertEqual(stop_loss.stop_price, Decimal(100.50))
        self.assertEqual(stop_loss.limit_price, Decimal(110.30))


class TakeProfitTests(TestCase):

    def test_create_asset_class(self):
        """Take profit object can be created."""
        take_profit = TakeProfit(
            limit_price=Decimal(110.30),
        )
        take_profit.save()

        self.assertIn(take_profit, TakeProfit.objects.all())
        self.assertEqual(take_profit.limit_price, Decimal(110.30))


class OrderTests(TestCase):

    def setUp(self):
        self.asset = AssetFactory(
            symbol='TEST'
        )
        self.stop_loss = StopLoss.objects.create(
            stop_price=Decimal(100.50)
            limit_price=Decimal(110.30)
        )
        self.take_profit = TakeProfit.objects.create(
            limit_price=Decimal(110.30)
        )

    def test_create_order(self):
        """A order object can be created."""
        client_order_id = uuid.uuid4()
        order = Order(
            status=Order.OPEN,
            symbol='TEST',
            quantity=100,
            side=Order.BUY,
            type=Order.MARKET,
            time_in_force=Order.DAY,
            client_order_id=client_order_id,
            # TO FINISH
        )
        order.save()

        # TO DO
