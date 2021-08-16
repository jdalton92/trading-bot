import uuid

from assets.tests.factories import AssetFactory
from core.tests.factories import StrategyFactory
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from orders.models import Order
from users.tests.factories import UserFactory

from .factories import OrderFactory

time_now = timezone.now()


@freeze_time(time_now)  # Freeze time for testing timedate fields
class OrderTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.order_1 = OrderFactory()
        self.order_2 = OrderFactory()
        self.order_3 = OrderFactory()
        self.order_4 = OrderFactory()
        self.asset = AssetFactory(symbol="TEST")
        self.strategy = StrategyFactory(asset=self.asset)

    def test_create_order(self):
        """A order object can be created."""
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
            hwm=95.7,
        )
        order.legs.add(self.order_3, self.order_4)
        order.save()

        self.assertIn(order, Order.objects.all())
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.strategy, self.strategy)
        self.assertEqual(str(order.id), str(uuid_1))
        self.assertEqual(str(order.client_order_id), str(uuid_2))
        self.assertEqual(order.created_at, time_now)
        self.assertEqual(order.updated_at, time_now)
        self.assertEqual(order.submitted_at, time_now)
        self.assertEqual(order.filled_at, time_now)
        self.assertEqual(order.canceled_at, time_now)
        self.assertEqual(order.failed_at, time_now)
        self.assertEqual(order.replaced_at, time_now)
        self.assertEqual(order.replaced_by, self.order_1)
        self.assertEqual(order.replaces, self.order_2)
        self.assertEqual(order.replaces, self.order_2)
        self.assertEqual(order.asset_id, self.asset)
        self.assertEqual(order.symbol, self.asset)
        self.assertEqual(order.asset_class, self.asset.asset_class)
        self.assertEqual(order.qty, 100)
        self.assertEqual(order.filled_qty, 100)
        self.assertEqual(order.type, Order.MARKET)
        self.assertEqual(order.side, Order.BUY)
        self.assertEqual(order.time_in_force, Order.DAY)
        self.assertEqual(order.limit_price, 110.05)
        self.assertEqual(order.stop_price, 90.05)
        self.assertEqual(order.filled_avg_price, 100)
        self.assertEqual(order.status, Order.FILLED)
        self.assertTrue(order.extended_hours)
        self.assertEqual(order.legs.count(), 2)
        self.assertEqual(order.trail_price, 100)
        self.assertEqual(order.trail_percentage, 50.05)
        self.assertEqual(order.hwm, 95.7)

    def test_create_invalid_strategy_order(self):
        """An order asset_id and strategy asset must be the same."""
        invalid_asset = AssetFactory()

        with self.assertRaisesRegex(
            ValidationError,
            "Strategy ``asset`` and order ``asset_id`` must be the same",
        ):
            OrderFactory(strategy=self.strategy, asset_id=invalid_asset)
