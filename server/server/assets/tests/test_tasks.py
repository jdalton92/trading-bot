from alpaca_trade_api.entity import Bar as AlpacaBar
from alpaca_trade_api.entity import Quote as AlpacaQuote
from django.test import TestCase
from server.assets.models import Asset, AssetClass, Bar, Exchange
from server.assets.tasks import get_quotes, update_assets, update_bars
from server.assets.tests.factories import AssetFactory


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

        update_assets(self.asset_data)

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

        update_assets(self.asset_data + self.asset_data)

        self.assertEqual(Exchange.objects.all().count(), 2)
        self.assertEqual(AssetClass.objects.all().count(), 1)
        self.assertEqual(Asset.objects.all().count(), 3)

    def test_get_quotes(self):
        """Latest quotes for list of symbols is fetched."""
        symbols = ["TSLA", "AAPL"]
        quotes = get_quotes(symbols)

        self.assertEqual(len(quotes), 2)
        self.assertTrue(isinstance(quotes["TSLA"], AlpacaQuote))
        self.assertTrue(isinstance(quotes["AAPL"], AlpacaQuote))

    def test_update_bars(self):
        """Latest bars for list of symbols is fetched and saved."""
        tesla = AssetFactory(symbol="TSLA")
        microsoft = AssetFactory(symbol="AAPL")
        symbols = [tesla.symbol, microsoft.symbol]
        bars = update_bars(symbols, '1D', 10)

        # Bars are fetched correctly
        self.assertEqual(len(bars), 2)
        self.assertTrue(isinstance(bars["TSLA"][0], AlpacaBar))
        self.assertTrue(isinstance(bars["AAPL"][0], AlpacaBar))

        # Bars are saved to db correctly
        self.assertEqual(Bar.objects.filter(asset=tesla).count(), 10)
        self.assertEqual(Bar.objects.filter(asset=microsoft).count(), 10)
