from unittest.mock import patch

from alpaca_trade_api.entity import Asset as AlpacaAsset
from alpaca_trade_api.entity import Bar as AlpacaBar
from alpaca_trade_api.entity import Quote as AlpacaQuote
from django.test import TestCase
from server.assets.models import Asset, AssetClass, Bar, Exchange
from server.assets.tasks import get_quotes, update_assets, update_bars
from server.assets.tests.factories import AssetFactory


class AssetTaskTests(TestCase):
    def setUp(self):
        self.tesla_quote = AlpacaQuote(
            {
                "askexchange": 15,
                "askprice": 700.06,
                "asksize": 1,
                "bidexchange": 15,
                "bidprice": 660,
                "bidsize": 1,
                "timestamp": 1614373192920000000,
            }
        )
        self.apple_quote = AlpacaQuote(
            {
                "askexchange": 17,
                "askprice": 135.6,
                "asksize": 1,
                "bidexchange": 9,
                "bidprice": 119.36,
                "bidsize": 100,
                "timestamp": 1614373766182000000,
            }
        )
        self.asset_data = [
            AlpacaAsset(
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
                    "easy_to_borrow": True,
                }
            ),
            AlpacaAsset(
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
                    "easy_to_borrow": False,
                }
            ),
            AlpacaAsset(
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
                    "easy_to_borrow": False,
                }
            ),
        ]
        self.bars = {
            "AAPL": [
                AlpacaBar(
                    {
                        "asset": "AAPL",
                        "c": 121,
                        "h": 126.4585,
                        "l": 120.54,
                        "o": 124.68,
                        "t": 1614229200,
                        "v": 134693926,
                    }
                ),
                AlpacaBar(
                    {
                        "asset": "AAPL",
                        "c": 121.2,
                        "h": 124.85,
                        "l": 121.2,
                        "o": 122.59,
                        "t": 1614315600,
                        "v": 135693674,
                    }
                ),
            ],
            "TSLA": [
                AlpacaBar(
                    {
                        "asset": "TSLA",
                        "c": 682.6,
                        "h": 737.2066,
                        "l": 670.58,
                        "o": 726.15,
                        "t": 1614229200,
                        "v": 36814146,
                    }
                ),
                AlpacaBar(
                    {
                        "asset": "TSLA",
                        "c": 671.01,
                        "h": 706.7,
                        "l": 659.51,
                        "o": 700,
                        "t": 1614315600,
                        "v": 36281006,
                    }
                ),
            ],
        }

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

    @patch("server.assets.tasks.TradeApiRest")
    def test_get_quotes(self, mock_api):
        """Latest quotes for list of symbols is fetched."""

        def alpaca_quote_response(symbol):
            if symbol == "TSLA":
                return self.tesla_quote
            if symbol == "AAPL":
                return self.apple_quote

        mock_api().get_last_quote.side_effect = alpaca_quote_response

        symbols = ["TSLA", "AAPL"]
        quotes = get_quotes(symbols)

        self.assertEqual(len(quotes), 2)
        self.assertEqual(quotes["TSLA"], self.tesla_quote)
        self.assertEqual(quotes["AAPL"], self.apple_quote)

    @patch("server.assets.tasks.TradeApiRest")
    def test_update_bars(self, mock_api):
        """Latest bars for list of symbols is fetched and saved."""
        mock_api().get_bars.return_value = self.bars

        tesla = AssetFactory(symbol="TSLA")
        microsoft = AssetFactory(symbol="AAPL")
        symbols = [tesla.symbol, microsoft.symbol]
        bars = update_bars(symbols=symbols, timeframe="1D", limit=2)

        # Bars are fetched
        self.assertEqual(len(bars), 2)
        self.assertTrue(isinstance(bars["TSLA"][0], AlpacaBar))
        self.assertTrue(isinstance(bars["AAPL"][0], AlpacaBar))

        # Bars are saved to db correctly
        self.assertEqual(Bar.objects.filter(asset=tesla).count(), 2)
        self.assertEqual(Bar.objects.filter(asset=microsoft).count(), 2)
