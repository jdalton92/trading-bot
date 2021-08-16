import uuid

from assets.tests.factories import AssetFactory
from core.tests.factories import StrategyFactory
from django.test import TestCase
from django.utils import timezone
from orders.models import Order
from orders.tasks import update_orders
from users.tests.factories import UserFactory


class OrderTaskTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.strategy = StrategyFactory()
        self.asset_1 = AssetFactory(symbol="AAPL")
        self.asset_2 = AssetFactory(symbol="TLSA")
        self.asset_3 = AssetFactory(symbol="MFST")
        self.uuid_1 = uuid.uuid4()
        self.uuid_2 = uuid.uuid4()
        self.uuid_3 = uuid.uuid4()
        self.uuid_4 = uuid.uuid4()
        self.uuid_5 = uuid.uuid4()
        self.uuid_6 = uuid.uuid4()
        self.order_data = [
            {
                "user": self.user.pk,
                "status": "filled",
                "asset_id": self.asset_1.pk,
                "symbol": self.asset_1.symbol,
                "qty": 10.01,
                "filled_qty": 10.01,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": self.uuid_1,
                "id": self.uuid_2,
                "created_at": timezone.now(),
            },
            {
                "user": self.user.pk,
                "status": "filled",
                "asset_id": self.asset_2.pk,
                "symbol": self.asset_2.symbol,
                "qty": 101.05,
                "filled_qty": 10.01,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": self.uuid_3,
                "id": self.uuid_4,
                "created_at": timezone.now(),
            },
            {
                "user": self.user.pk,
                "status": "filled",
                "asset_id": self.asset_3.pk,
                "symbol": self.asset_3.symbol,
                "qty": 105.08,
                "filled_qty": 10.01,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": self.uuid_5,
                "id": self.uuid_6,
                "created_at": timezone.now(),
            },
        ]

    def test_add_orders(self):
        """Order data is updated."""
        self.assertEqual(Order.objects.all().count(), 0)

        update_orders(self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)

    def test_add_duplicate_orders(self):
        """Duplicate order data is not updated."""
        self.assertEqual(Order.objects.all().count(), 0)

        update_orders(self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)

        # Adding duplicate order_data should not save to db
        update_orders(self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)
