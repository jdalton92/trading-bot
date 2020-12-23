from django.test import TestCase
from server.assets.tests.factories import AssetFactory
from server.core.tests.factories import StrategyFactory
from server.orders.models import Order
from server.orders.tasks import update_orders
from server.users.tests.factories import UserFactory


class OrderTaskTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.strategy = StrategyFactory()
        self.asset_1 = AssetFactory(symbol="AAPL")
        self.asset_2 = AssetFactory(symbol="TLSA")
        self.asset_3 = AssetFactory(symbol="MFST")
        self.order_data = [
            {
                "user": self.user.pk,
                "status": "open",
                "symbol": "AAPL",
                "quantity": 10.01,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": "a8d52afb-b645-4d69-abfb-5e4810bd8c05"
            },
            {
                "user": self.user.pk,
                "status": "open",
                "symbol": "TLSA",
                "quantity": 101.05,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": "5bd31df8-802a-47c5-b385-49425b57f9da"
            },
            {
                "user": self.user.pk,
                "status": "open",
                "symbol": "MFST",
                "quantity": 105.08,
                "side": "buy",
                "type": "market",
                "time_in_force": "day",
                "client_order_id": "28664ba6-6d3e-40a6-a679-f633d38981ef"
            }
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
