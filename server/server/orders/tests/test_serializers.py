import uuid
from decimal import Decimal

from django.test import TestCase
from django.test.client import RequestFactory
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order
from server.orders.serializers import OrderCreateSerializer, OrderSerializer
from server.users.serializers import UserSerializer
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory


class OrderSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def setUp(self):
        self.user = UserFactory()

    def test_view_order(self):
        """Order data is serialized correctly."""
        asset = AssetFactory(symbol='TEST')
        order = Order(
            user=self.user,
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

        self.assertEqual(
            data['user'],
            UserSerializer(
                self.user,
                fields=("id", "first_name", "last_name")
            ).data
        )
        self.assertEqual(data['status'], Order.OPEN)
        self.assertEqual(data['symbol'], 'TEST')
        self.assertEqual(float(data['quantity']), 100.05)
        self.assertEqual(data['side'], Order.BUY)
        self.assertEqual(data['type'], Order.MARKET)
        self.assertEqual(data['time_in_force'], Order.DAY)

    def test_create_order(self):
        """Order data is saved correctly for admins."""
        AssetFactory(symbol='TEST')
        client_order_id = uuid.uuid4()
        data = {
            "user": self.user.pk,
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

        self.assertEqual(self.user, order.user)
        self.assertEqual(data['status'], order.status)
        self.assertEqual(data['symbol'], order.symbol.symbol)
        self.assertEqual(data['quantity'], float(order.quantity))
        self.assertEqual(data['side'], order.side)
        self.assertEqual(data['type'], order.type)
        self.assertEqual(data['time_in_force'], order.time_in_force)
        self.assertEqual(data['client_order_id'], str(order.client_order_id))
        self.assertEqual(data['limit_price'], float(order.limit_price))
        self.assertEqual(data['stop_price'], float(order.stop_price))
        self.assertEqual(data['trail_price'], float(order.trail_price))
        self.assertEqual(
            data['trail_percentage'],
            float(order.trail_percentage)
        )
        self.assertTrue(order.extended_hours)
        self.assertEqual(data['order_class'], order.order_class)
        self.assertEqual(data['take_profit'], order.take_profit)
        self.assertEqual(
            data['stop_loss'],
            order.stop_loss
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
