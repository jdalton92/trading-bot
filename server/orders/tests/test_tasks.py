import uuid

from alpaca_trade_api.entity import Order as AlpacaOrder
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
        self.uuid_1 = str(uuid.uuid4())
        self.uuid_2 = str(uuid.uuid4())
        self.uuid_3 = str(uuid.uuid4())
        self.uuid_4 = str(uuid.uuid4())
        self.uuid_5 = str(uuid.uuid4())
        self.uuid_6 = str(uuid.uuid4())
        self.order_data = [
            AlpacaOrder(
                {
                    "status": "filled",
                    "asset_id": self.asset_1.pk,
                    "symbol": self.asset_1.symbol,
                    "asset_class": self.asset_1.asset_class.name,
                    "qty": 10.01,
                    "filled_qty": 10.01,
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "day",
                    "client_order_id": self.uuid_1,
                    "id": self.uuid_2,
                    "created_at": str(timezone.now()),
                }
            ),
            AlpacaOrder(
                {
                    "status": "filled",
                    "asset_id": self.asset_2.pk,
                    "symbol": self.asset_2.symbol,
                    "asset_class": self.asset_1.asset_class.name,
                    "qty": 101.05,
                    "filled_qty": 10.01,
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "day",
                    "client_order_id": self.uuid_3,
                    "id": self.uuid_4,
                    "created_at": str(timezone.now()),
                }
            ),
            AlpacaOrder(
                {
                    "status": "filled",
                    "asset_id": self.asset_3.pk,
                    "symbol": self.asset_3.symbol,
                    "asset_class": self.asset_1.asset_class.name,
                    "qty": 105.08,
                    "filled_qty": 10.01,
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "day",
                    "client_order_id": self.uuid_5,
                    "id": self.uuid_6,
                    "created_at": str(timezone.now()),
                }
            ),
        ]

    def test_add_orders(self):
        """Order data is updated."""
        self.assertEqual(Order.objects.all().count(), 0)

        update_orders(self.user, self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)

    def test_add_duplicate_orders(self):
        """Duplicate order data is not updated."""
        self.assertEqual(Order.objects.all().count(), 0)

        update_orders(self.user, self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)

        # Adding duplicate order_data should not save to db
        update_orders(self.user, self.order_data)

        self.assertEqual(Order.objects.all().count(), 3)
