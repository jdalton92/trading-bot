import uuid

from django.test import TestCase
from django.test.client import RequestFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order, StopLoss, TakeProfit
from server.orders.serializers import (OrderCreateSerializer, OrderSerializer,
                                       StopLossSerializer,
                                       TakeProfitSerializer)
from server.users.tests.factories import AdminFactory

from .factories import OrderFactory, StopLossFactory, TakeProfitFactory


class StopLossSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def test_view_stop_loss(self):
        """Stop loss data is serialized correctly."""
        stop_loss = StopLossFactory()
        data = StopLossSerializer(
            stop_loss, context={'request': self.request}
        ).data

        self.assertEqual(
            float(data['stop_price']),
            float(stop_loss.stop_price)
        )
        self.assertEqual(
            float(data['limit_price']),
            float(stop_loss.limit_price)
        )

    def test_create_stop_loss(self):
        """Stop loss data is saved correctly."""
        data = {
            "stop_price": 100.05,
            "limit_price": 110.05,
        }

        serializer = StopLossSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())
        stop_loss = serializer.save()

        self.assertEqual(
            data['stop_price'],
            float(stop_loss.stop_price)
        )
        self.assertEqual(
            data['limit_price'],
            float(stop_loss.limit_price)
        )

    def test_update_stop_loss(self):
        """Stop loss data is updated correctly."""
        stop_loss = StopLossFactory(stop_price=100.01)
        serializer = StopLossSerializer(
            stop_loss,
            data={'stop_price': 100.05},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        stop_loss.refresh_from_db()
        self.assertEqual(
            float(stop_loss.stop_price),
            100.05
        )


class TakeProfitSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def test_view_take_profit(self):
        """Take profit data is serialized correctly."""
        take_profit = TakeProfitFactory()
        data = TakeProfitSerializer(
            take_profit, context={'request': self.request}
        ).data

        self.assertEqual(
            float(data['limit_price']),
            float(take_profit.limit_price)
        )

    def test_create_take_profit(self):
        """Take profit data is saved correctly."""
        data = {
            "limit_price": 110.05,
        }

        serializer = TakeProfitSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())
        take_profit = serializer.save()

        self.assertEqual(
            data['limit_price'],
            float(take_profit.limit_price)
        )

    def test_update_take_profit(self):
        """Take profit data is updated correctly."""
        take_profit = TakeProfitFactory(limit_price=100.01)
        serializer = TakeProfitSerializer(
            take_profit,
            data={'limit_price': 100.05},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        take_profit.refresh_from_db()
        self.assertEqual(
            float(take_profit.limit_price),
            100.05
        )


class OrderSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def setUp(self):
        self.stop_loss = StopLossFactory(
            stop_price=100.50,
            limit_price=110.30
        )
        self.take_profit = TakeProfitFactory(
            limit_price=110.30
        )

    def test_view_order(self):
        """Order data is serialized correctly."""
        asset = AssetFactory(symbol='TEST')
        order = OrderFactory(
            status=Order.OPEN,
            symbol=asset,
            quantity=100.05,
            side=Order.BUY,
            type=Order.MARKET,
            time_in_force=Order.DAY
        )
        data = OrderSerializer(
            order, context={'request': self.request}
        ).data

        self.assertIn(order, Order.objects.all())
        self.assertEqual(order.status, Order.OPEN)
        self.assertEqual(order.symbol.symbol, 'TEST')
        self.assertEqual(float(order.quantity), 100.05)
        self.assertEqual(order.side, Order.BUY)
        self.assertEqual(order.type, Order.MARKET)
        self.assertEqual(order.time_in_force, Order.DAY)

    def test_create_order(self):
        """Order data is saved correctly for admins."""
        asset = AssetFactory(symbol='TEST')
        client_order_id = uuid.uuid4()
        data = {
            "status": "open",
            "symbol": "TEST",
            "quantity": 100.05,
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "client_order_id": str(client_order_id),
            "limit_price": 110.05,
            "stop_price": 90.05,
            "trail_price": 100.05,
            "trail_percentage": 50.05,
            "extended_hours": True,
            "order_class": "simple",
            "take_profit": {
                "limit_price": 100.05
            },
            "stop_loss": {
                "stop_price": 100.01,
                "limit_price": 100.05
            },
        }

        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        order = serializer.save()

        self.assertEqual(data['status'], Order.OPEN)
        self.assertEqual(data['symbol'], 'TEST')
        self.assertEqual(data['quantity'], 100.05)
        self.assertEqual(data['side'], Order.BUY)
        self.assertEqual(data['type'], Order.MARKET)
        self.assertEqual(data['time_in_force'], Order.DAY)
        self.assertEqual(data['client_order_id'], str(client_order_id))
        self.assertEqual(data['limit_price'], 110.05)
        self.assertEqual(data['stop_price'], 90.05)
        self.assertEqual(data['trail_price'], 100.05)
        self.assertEqual(data['trail_percentage'], 50.05)
        self.assertTrue(data['extended_hours'])
        self.assertEqual(data['order_class'], Order.SIMPLE)
        self.assertEqual(data['take_profit'], {"limit_price": 100.05})
        self.assertEqual(
            data['stop_loss'],
            {"stop_price": 100.01, "limit_price": 100.05}
        )

    def test_update_order(self):
        """Order data is updated correctly for admins."""
        order = OrderFactory(status='open')
        serializer = OrderCreateSerializer(
            order,
            data={'status': 'closed'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        order.refresh_from_db()
        self.assertEqual(
            order.status,
            'closed'
        )
