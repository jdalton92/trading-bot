from django.test import TestCase
from server.assets.models import Asset, AssetClass, Exchange
from server.assets.tasks import update_asset_models


class AssetTaskTests(TestCase):

    def setUp(self):
        self.asset_data = [
            {
                "id": "5e947a98-f3a2-4950-b0dc-d3f3696bac59",
                "class": "us_equity",
                "exchange": "NASDAQ",
                "symbol": "CRON",
                "name": "Cronos Group Inc. Common Share",
                "status": "active",
                "tradable": True,
                "marginable": True,
                "shortable": True,
                "easy_to_borrow": True
            },
            {
                "id": "951d6ad0-d0b6-42c0-aad5-e1587f933846",
                "class": "us_equity",
                "exchange": "ARCA",
                "symbol": "GBUY",
                "name": "Goldman Sachs New Age Consumer ETF",
                "status": "inactive",
                "tradable": False,
                "marginable": False,
                "shortable": False,
                "easy_to_borrow": False
            },
            {
                "id": "98f808ab-c0ad-41a2-ae91-e1f908a5c7d0",
                "class": "us_equity",
                "exchange": "NASDAQ",
                "symbol": "KBLMU",
                "name": "KBL Merger Corp. IV Unit",
                "status": "inactive",
                "tradable": False,
                "marginable": False,
                "shortable": False,
                "easy_to_borrow": False
            }
        ]

    def test_add_asset(self):
        """Asset, asset class, and exchange data is updated."""
        self.assertEqual(Exchange.objects.all().count(), 0)
        self.assertEqual(AssetClass.objects.all().count(), 0)
        self.assertEqual(Asset.objects.all().count(), 0)

        update_asset_models(self.asset_data)

        self.assertEqual(Exchange.objects.all().count(), 2)
        self.assertEqual(AssetClass.objects.all().count(), 1)
        self.assertEqual(Asset.objects.all().count(), 3)

    def test_add_duplicate_assets(self):
        """
        Duplicate asset, asset class, and exchange data is not created if it
        already exists.
        """

        self.assertEqual(Exchange.objects.all().count(), 0)
        self.assertEqual(AssetClass.objects.all().count(), 0)
        self.assertEqual(Asset.objects.all().count(), 0)

        update_asset_models(self.asset_data + self.asset_data)

        self.assertEqual(Exchange.objects.all().count(), 2)
        self.assertEqual(AssetClass.objects.all().count(), 1)
        self.assertEqual(Asset.objects.all().count(), 3)
