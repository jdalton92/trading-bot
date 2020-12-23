import uuid
from decimal import Decimal

from django.test import TestCase
from django.test.client import RequestFactory
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
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
        self.asset = AssetFactory(symbol='AAPL')
        self.strategy = StrategyFactory(asset=self.asset)
        self.user = UserFactory()

    def test_view_order(self):
        """Order data is serialized correctly."""
        order = Order(
            user=self.user,
            strategy=self.strategy,
            status=Order.OPEN,
            symbol=self.asset,
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
        self.assertEqual(data['strategy'], self.strategy.type)
        self.assertEqual(data['status'], Order.OPEN)
        self.assertEqual(data['symbol'], 'AAPL')
        self.assertEqual(float(data['quantity']), 100.05)
        self.assertEqual(data['side'], Order.BUY)
        self.assertEqual(data['type'], Order.MARKET)
        self.assertEqual(data['time_in_force'], Order.DAY)

    def test_create_order(self):
        """Order data is saved correctly for admins."""
        client_order_id = uuid.uuid4()
        data = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
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
        self.assertEqual(self.strategy, order.strategy)
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

    def test_create_limit_order_invalid(self):
        """Incorrect limit orders raise validations errors."""
        data = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "buy",
            "type": "limit",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['limit_price'][0]),
            "Field is required if `type` is `stop_limit` or `limit`"
        )

        data['limit_price'] = 100
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_create_stop_order_invalid(self):
        """Incorrect stop orders raise validations errors."""
        data = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "buy",
            "type": "stop",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['stop_price'][0]),
            "Field is required if `type` is `stop` or `stop_limit`"
        )

        data['stop_price'] = 100
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_create_trailing_stop_order_invalid(self):
        """Incorrect trailing stop orders raise validations errors."""
        data = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "buy",
            "type": "trailing_stop",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['trail_price'][0]),
            "Either `trail_price` or `trail_percentage` is required if `type` "
            "is `trailing_stop`"
        )
        self.assertEqual(
            str(serializer.errors['trail_percent'][0]),
            "Either `trail_price` or `trail_percentage` is required if `type` "
            "is `trailing_stop`"
        )

        data['trail_price'] = 100
        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

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
