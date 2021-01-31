import uuid
from datetime import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from freezegun import freeze_time
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
from server.orders.models import Order
from server.orders.serializers import (OrderCreateSerializer,
                                       OrderPostSerializer, OrderSerializer)
from server.users.serializers import UserSerializer
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory

time_now = '2021-01-30T05:25:22.831798Z'


@freeze_time(time_now)  # Freeze time for testing timedate fields
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
        self.order_1 = OrderFactory()
        self.order_2 = OrderFactory()
        self.order_3 = OrderFactory()
        self.order_4 = OrderFactory()

    def test_post_order(self):
        """Order data is valid for posting to alpaca api."""
        client_order_id = uuid.uuid4()
        data = {
            "symbol": "AAPL",
            "qty": 100.05,
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

        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_post_limit_order_invalid(self):
        """Incorrect limit orders raise validations errors."""
        data = {
            "symbol": "AAPL",
            "qty": 100.05,
            "side": "buy",
            "type": "limit",
            "time_in_force": "day",
            "order_class": "simple",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['limit_price'][0]),
            "Field is required if `type` is `stop_limit` or `limit`"
        )

        data['limit_price'] = 100
        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_post_stop_order_invalid(self):
        """Incorrect stop orders raise validations errors."""
        data = {
            "symbol": "AAPL",
            "qty": 100.05,
            "side": "buy",
            "type": "stop",
            "time_in_force": "day",
            "order_class": "simple",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors['stop_price'][0]),
            "Field is required if `type` is `stop` or `stop_limit`"
        )

        data['stop_price'] = 100
        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_post_trailing_stop_order_invalid(self):
        """Incorrect trailing stop orders raise validations errors."""
        data = {
            "symbol": "AAPL",
            "qty": 100.05,
            "side": "buy",
            "type": "trailing_stop",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        serializer = OrderPostSerializer(
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
        serializer = OrderPostSerializer(
            data=data,
            context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())

    def test_view_order(self):
        """
        Order returned from alpaca api is serialized for viewing correctly.
        """
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()
        order = Order(
            user=self.user,
            strategy=self.strategy,
            id=uuid_1,
            client_order_id=uuid_2,
            created_at=time_now,
            updated_at=time_now,
            submitted_at=time_now,
            filled_at=time_now,
            expired_at=time_now,
            canceled_at=time_now,
            failed_at=time_now,
            replaced_at=time_now,
            replaced_by=self.order_1,
            replaces=self.order_2,
            asset_id=self.asset,
            qty=100,
            filled_qty=100,
            type=Order.MARKET,
            side=Order.BUY,
            time_in_force=Order.DAY,
            limit_price=110.05,
            stop_price=90.05,
            filled_avg_price=100,
            status=Order.FILLED,
            extended_hours=True,
            trail_price=100,
            trail_percentage=50.05,
            hwm=95.7
        )
        order.legs.add(self.order_3, self.order_4)
        order.save()

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
        self.assertEqual(str(data['id']), str(uuid_1))
        self.assertEqual(str(data['client_order_id']), str(uuid_2))
        self.assertEqual(data['created_at'], time_now)
        self.assertEqual(data['updated_at'], time_now)
        self.assertEqual(data['submitted_at'], time_now)
        self.assertEqual(data['filled_at'], time_now)
        self.assertEqual(data['canceled_at'], time_now)
        self.assertEqual(data['failed_at'], time_now)
        self.assertEqual(data['replaced_at'], time_now)
        self.assertEqual(data['replaced_by'], self.order_1.pk)
        self.assertEqual(data['replaces'], self.order_2.pk)
        self.assertEqual(data['replaces'], self.order_2.pk)
        self.assertEqual(data['asset_id'], self.asset.pk)
        self.assertEqual(data['symbol'], self.asset.symbol)
        self.assertEqual(data['asset_class'], self.asset.asset_class.name)
        self.assertEqual(float(data['qty']), 100)
        self.assertEqual(float(data['filled_qty']), 100)
        self.assertEqual(data['type'], Order.MARKET)
        self.assertEqual(data['side'], Order.BUY)
        self.assertEqual(data['time_in_force'], Order.DAY)
        self.assertEqual(float(data['limit_price']), 110.05)
        self.assertEqual(float(data['stop_price']), 90.05)
        self.assertEqual(float(data['filled_avg_price']), 100)
        self.assertEqual(data['status'], Order.FILLED)
        self.assertTrue(data['extended_hours'])
        self.assertEqual(len(data['legs']), 2)
        self.assertEqual(
            data['legs'][0],
            OrderSerializer(
                self.order_3,
                fields=('id', 'symbol', 'side', 'qty'),
            ).data
        )
        self.assertEqual(
            data['legs'][1],
            OrderSerializer(
                self.order_4,
                fields=('id', 'symbol', 'side', 'qty'),
            ).data
        )
        self.assertEqual(float(data['trail_price']), 100)
        self.assertEqual(float(data['trail_percentage']), 50.05)
        self.assertEqual(float(data['hwm']), 95.7)

    def test_create_order(self):
        """Order data is saved correctly for admins."""
        uuid_1 = uuid.uuid4()
        uuid_2 = uuid.uuid4()
        data = {
            "user": self.user.pk,
            "strategy": self.strategy.pk,
            "id": uuid_1,
            "client_order_id": uuid_2,
            "created_at": time_now,
            "updated_at": time_now,
            "submitted_at": time_now,
            "filled_at": time_now,
            "expired_at": time_now,
            "canceled_at": time_now,
            "failed_at": time_now,
            "replaced_at": time_now,
            "replaced_by": self.order_1.pk,
            "replaces": self.order_2.pk,
            "asset_id": self.asset.pk,
            "symbol": self.asset.symbol,
            "asset_class": self.asset.asset_class.name,
            "legs": [
                self.order_3.pk, self.order_4.pk
            ],
            "qty": 100,
            "filled_qty": 100,
            "type": Order.MARKET,
            "side": Order.BUY,
            "time_in_force": Order.DAY,
            "limit_price": 110.05,
            "stop_price": 90.05,
            "filled_avg_price": 100,
            "status": Order.FILLED,
            "extended_hours": True,
            "trail_price": 100,
            "trail_percentage": 50.05,
            "hwm": 95.7
        }

        serializer = OrderCreateSerializer(
            data=data,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())

        order = serializer.save()

        self.assertEqual(data['id'], order.id)
        self.assertEqual(data['user'], order.user.pk)
        self.assertEqual(data['strategy'], order.strategy.pk)
        self.assertEqual(str(data['id']), str(uuid_1))
        self.assertEqual(str(data['client_order_id']), str(uuid_2))
        self.assertEqual(data['created_at'], time_now)
        self.assertEqual(data['updated_at'], time_now)
        self.assertEqual(data['submitted_at'], time_now)
        self.assertEqual(data['filled_at'], time_now)
        self.assertEqual(data['canceled_at'], time_now)
        self.assertEqual(data['failed_at'], time_now)
        self.assertEqual(data['replaced_at'], time_now)
        self.assertEqual(data['replaced_by'], self.order_1.pk)
        self.assertEqual(data['replaces'], self.order_2.pk)
        self.assertEqual(data['replaces'], self.order_2.pk)
        self.assertEqual(data['asset_id'], self.asset.pk)
        self.assertEqual(data['symbol'], self.asset.symbol)
        self.assertEqual(data['asset_class'], order.asset_id.asset_class.name)
        self.assertEqual(float(data['qty']), 100)
        self.assertEqual(float(data['filled_qty']), 100)
        self.assertEqual(data['type'], Order.MARKET)
        self.assertEqual(data['side'], Order.BUY)
        self.assertEqual(data['time_in_force'], Order.DAY)
        self.assertEqual(float(data['limit_price']), 110.05)
        self.assertEqual(float(data['stop_price']), 90.05)
        self.assertEqual(float(data['filled_avg_price']), 100)
        self.assertEqual(data['status'], Order.FILLED)
        self.assertTrue(data['extended_hours'])
        self.assertEqual(len(data['legs']), 2)
        self.assertEqual(float(data['trail_price']), 100)
        self.assertEqual(float(data['trail_percentage']), 50.05)
        self.assertEqual(float(data['hwm']), 95.7)

    def test_update_order(self):
        """Order data returned from alpaca is updated correctly for admins."""
        order = OrderFactory(status='open')
        serializer = OrderCreateSerializer(
            order,
            data={'status': 'partially_filled'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.is_valid()

        serializer.save()

        order.refresh_from_db()
        self.assertEqual(
            order.status,
            'partially_filled'
        )
