import json
import uuid
from datetime import timedelta
from unittest.mock import patch

from alpaca_trade_api.entity import Account as AlpacaAccount
from alpaca_trade_api.entity import Order as AlpacaOrder
from alpaca_trade_api.entity import Position as AlpacaPosition
from assets.models import Asset, Bar
from assets.tests.factories import AssetFactory
from core.tasks import (
    fetch_bar_data_for_strategy,
    moving_average_strategy,
    run_strategies_for_users,
)
from core.tests.factories import StrategyFactory
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from orders.models import Order
from users.tests.factories import UserFactory


class CoreTaskTests(TestCase):
    def setUp(self):
        self.tsla = AssetFactory(symbol="TSLA")
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.user_3 = UserFactory()
        self.strategy_1 = StrategyFactory(
            asset=self.tsla, user=self.user_1, trade_value=1000
        )
        self.strategy_2 = StrategyFactory(
            asset=self.tsla, user=self.user_2, trade_value=1000
        )
        self.inactive_strategy = StrategyFactory(
            user=self.user_3,
            start_date=timezone.now() - timedelta(days=7),
            end_date=timezone.now() - timedelta(days=5),
        )

    def refresh_tsla_bars(self, max_epoch=1648443600):
        tsla = Asset.objects.get(symbol="TSLA")
        Bar.objects.filter(asset=tsla).delete()
        with open("assets/tests/sample_tsla_bars.json") as f:
            bars = json.load(f)
            objs = [
                Bar(
                    asset=tsla,
                    t=bar["t"],
                    o=bar["o"],
                    h=bar["h"],
                    l=bar["l"],
                    c=bar["c"],
                    v=bar["v"],
                )
                for bar in bars
                if int(bar["t"]) <= max_epoch
            ]
            Bar.objects.bulk_create(objs, batch_size=1000, ignore_conflicts=True)

    @patch("core.tasks.TradeApiRest")
    @patch("core.tasks.moving_average_strategy")
    def test_run_strategies_for_user(
        self, mock_moving_average_strategy, mock_trade_api
    ):
        """Moving average strategies that are active are run for users."""
        mock_trade_api.return_value.is_market_open.return_value = True

        run_strategies_for_users()

        self.assertEqual(mock_moving_average_strategy.call_count, 2)
        mock_moving_average_strategy.assert_any_call(self.user_1)
        mock_moving_average_strategy.assert_any_call(self.user_2)

    @patch("core.tasks.logger")
    @patch("core.tasks.fetch_bar_data_for_strategy")
    @patch("core.tasks.update_bars")
    @patch("core.tasks.TradeApiRest")
    def test_moving_average_strategy_not_enough_data(
        self,
        mock_trade_api,
        mock_update_bars,
        mock_fetch_bar_data_for_strategy,
        mock_logger,
    ):
        """Active strategy does not create an order if there is not enough bar data."""
        mock_fetch_bar_data_for_strategy.return_value = None

        moving_average_strategy(self.user_1)
        mock_logger.info.assert_called_once_with(
            f"Insufficient bar data for asset: {self.strategy_1.asset.id}"
        )

    @patch("core.tasks.time.mktime")
    @patch("core.tasks.update_bars")
    def test_fetch_bar_data_for_strategy(self, mock_update_bars, mock_mktime):
        """Bar data is fetched when required."""
        self.refresh_tsla_bars()

        with self.subTest(msg="bar data is not required."):
            # Enough bar data exists in sample data at this time
            mock_mktime.return_value = "1614229200"
            fetch_bar_data_for_strategy(self.strategy_1)
            mock_update_bars.assert_not_called()

        mock_mktime.reset_mock()
        mock_update_bars.reset_mock()

        with self.subTest(msg="bar data is required."):
            # Not enough bar data exists in sample data at this time
            mock_mktime.return_value = "1648443600"
            fetch_bar_data_for_strategy(self.strategy_1)
            mock_update_bars.assert_called_once_with(["TSLA"], "15Min", 131)

    @patch("core.tasks.TradeApiRest")
    @patch("core.tasks.time.mktime")
    @patch("core.tasks.update_bars")
    @patch("core.tasks.fetch_bar_data_for_strategy")
    def test_moving_average_strategy(
        self,
        mock_fetch_bar_data_for_strategy,
        mock_update_bars,
        mock_mktime,
        mock_trade_api,
    ):
        """Active strategy creates an order if required."""
        account_info = AlpacaAccount(
            {
                "account_blocked": False,
                "account_number": "GS78FJEUMA4P",
                "buying_power": "200000",
                "cash": "100000",
                "created_at": "2020-10-31T23:40:50.376107Z",
                "currency": "USD",
                "daytrade_count": 0,
                "daytrading_buying_power": "0",
                "equity": "100000",
                "id": str(uuid.uuid4()),
                "initial_margin": "0",
                "last_equity": "100000",
                "last_maintenance_margin": "0",
                "long_market_value": "0",
                "maintenance_margin": "0",
                "multiplier": "2",
                "non_marginable_buying_power": "100000",
                "pattern_day_trader": True,
                "pending_transfer_in": "0",
                "portfolio_value": "100000",
                "regt_buying_power": "200000",
                "short_market_value": "0",
                "shorting_enabled": True,
                "sma": "0",
                "status": "ACTIVE",
                "trade_suspended_by_user": False,
                "trading_blocked": False,
                "transfers_blocked": False,
            }
        )
        position = AlpacaPosition(
            {
                "asset_id": "0",
                "symbol": "TSLA",
                "exchange": "0",
                "asset_class": "0",
                "avg_entry_price": "0",
                "qty": "10",
                "side": "long",
                "market_value": "2000.0",
                "cost_basis": "0",
                "unrealized_pl": "0",
                "unrealized_plpc": "0",
                "unrealized_intraday_pl": "0",
                "unrealized_intraday_plpc": "0",
                "current_price": "0",
                "lastday_price": "0",
                "change_today": "0",
            }
        )
        order = AlpacaOrder(
            {
                "id": str(uuid.uuid4()),
                "client_order_id": str(uuid.uuid4()),
                "created_at": "2021-03-16T18:38:01.942282Z",
                "updated_at": "2021-03-16T18:38:01.942282Z",
                "submitted_at": "2021-03-16T18:38:01.937734Z",
                "filled_at": None,
                "expired_at": None,
                "canceled_at": None,
                "failed_at": None,
                "replaced_at": None,
                "replaced_by": None,
                "replaces": None,
                "asset_id": self.tsla.pk,
                "symbol": "TSLA",
                "asset_class": "us_equity",
                "notional": "500",
                "qty": None,
                "filled_qty": "0",
                "filled_avg_price": None,
                "order_class": "",
                "order_type": "market",
                "type": "market",
                "side": "buy",
                "time_in_force": "day",
                "limit_price": None,
                "stop_price": None,
                "status": "accepted",
                "extended_hours": False,
                "trail_percent": None,
                "trail_price": None,
                "hwm": None,
            }
        )

        mock_fetch_bar_data_for_strategy.return_value = 130
        mock_trade_api.return_value.is_market_open.return_value = True
        mock_trade_api.return_value.account_info.return_value = account_info
        mock_trade_api.return_value.list_position_by_symbol.return_value = position
        mock_trade_api.return_value.submit_order.return_value = order

        seven_days_epoch = 104 * 86400
        with self.subTest(msg="buy order is placed."):
            max_epoch_time = 1630818000
            base_epoch = max_epoch_time - seven_days_epoch
            mock_mktime.return_value = base_epoch
            self.refresh_tsla_bars(max_epoch=max_epoch_time)
            moving_average_strategy(self.user_1)
            mock_trade_api.return_value.submit_order.assert_called_once_with(
                symbol=self.strategy_1.asset.symbol,
                notional=float(self.strategy_1.trade_value),
                side=Order.BUY,
                type=Order.MARKET,
                time_in_force=Order.GTC,
            )

        mock_mktime.reset_mock()
        mock_trade_api.reset_mock()
        Order.objects.all().delete()

        with self.subTest(msg="sell order is placed."):
            max_epoch_time = 1618894800
            base_epoch = max_epoch_time - seven_days_epoch
            mock_mktime.return_value = base_epoch
            self.refresh_tsla_bars(max_epoch=max_epoch_time)
            moving_average_strategy(self.user_1)
            mock_trade_api.return_value.submit_order.assert_called_once_with(
                symbol=self.strategy_1.asset.symbol,
                notional=float(self.strategy_1.trade_value),
                side=Order.SELL,
                type=Order.MARKET,
                time_in_force=Order.GTC,
            )

        mock_mktime.reset_mock()
        mock_trade_api.reset_mock()
        Order.objects.all().delete()

        with self.subTest(msg="no order is placed."):
            max_epoch_time = 1633150800
            base_epoch = max_epoch_time - seven_days_epoch
            mock_mktime.return_value = base_epoch
            self.refresh_tsla_bars(max_epoch=max_epoch_time)
            moving_average_strategy(self.user_1)
            mock_trade_api.return_value.submit_order.assert_not_called()

    @patch("core.tasks.logger")
    @patch("core.tasks.TradeApiRest")
    @patch("core.tasks.time.mktime")
    @patch("core.tasks.update_bars")
    @patch("core.tasks.fetch_bar_data_for_strategy")
    def test_moving_average_strategy_fails(
        self,
        mock_fetch_bar_data_for_strategy,
        mock_update_bars,
        mock_mktime,
        mock_trade_api,
        mock_logger,
    ):
        """If trade view api fails to submit an order, an order object is not created."""
        account_info = AlpacaAccount(
            {
                "account_blocked": False,
                "account_number": "GS78FJEUMA4P",
                "buying_power": "200000",
                "cash": "100000",
                "created_at": "2020-10-31T23:40:50.376107Z",
                "currency": "USD",
                "daytrade_count": 0,
                "daytrading_buying_power": "0",
                "equity": "100000",
                "id": str(uuid.uuid4()),
                "initial_margin": "0",
                "last_equity": "100000",
                "last_maintenance_margin": "0",
                "long_market_value": "0",
                "maintenance_margin": "0",
                "multiplier": "2",
                "non_marginable_buying_power": "100000",
                "pattern_day_trader": True,
                "pending_transfer_in": "0",
                "portfolio_value": "100000",
                "regt_buying_power": "200000",
                "short_market_value": "0",
                "shorting_enabled": True,
                "sma": "0",
                "status": "ACTIVE",
                "trade_suspended_by_user": False,
                "trading_blocked": False,
                "transfers_blocked": False,
            }
        )
        position = AlpacaPosition(
            {
                "asset_id": "0",
                "symbol": "TSLA",
                "exchange": "0",
                "asset_class": "0",
                "avg_entry_price": "0",
                "qty": "10",
                "side": "long",
                "market_value": "2000.0",
                "cost_basis": "0",
                "unrealized_pl": "0",
                "unrealized_plpc": "0",
                "unrealized_intraday_pl": "0",
                "unrealized_intraday_plpc": "0",
                "current_price": "0",
                "lastday_price": "0",
                "change_today": "0",
            }
        )
        order = AlpacaOrder(
            {
                "id": str(uuid.uuid4()),
                "client_order_id": str(uuid.uuid4()),
                "created_at": "2021-03-16T18:38:01.942282Z",
                "updated_at": "2021-03-16T18:38:01.942282Z",
                "submitted_at": "2021-03-16T18:38:01.937734Z",
                "filled_at": None,
                "expired_at": None,
                "canceled_at": None,
                "failed_at": None,
                "replaced_at": None,
                "replaced_by": None,
                "replaces": None,
                "asset_id": self.tsla.pk,
                "symbol": "TSLA",
                "asset_class": "us_equity",
                "notional": "500",
                "qty": None,
                "filled_qty": "0",
                "filled_avg_price": None,
                "order_class": "",
                "order_type": "market",
                "type": "market",
                "side": "buy",
                "time_in_force": "day",
                "limit_price": None,
                "stop_price": None,
                "status": "accepted",
                "extended_hours": False,
                "trail_percent": None,
                "trail_price": None,
                "hwm": None,
            }
        )

        mock_fetch_bar_data_for_strategy.return_value = 130
        mock_trade_api.return_value.is_market_open.return_value = True
        mock_trade_api.return_value.account_info.return_value = account_info
        mock_trade_api.return_value.list_position_by_symbol.return_value = position
        mock_trade_api.return_value.submit_order.side_effect = ValidationError(
            "Mock error"
        )

        seven_days_epoch = 104 * 86400
        max_epoch_time = 1630818000
        base_epoch = max_epoch_time - seven_days_epoch
        mock_mktime.return_value = base_epoch
        self.refresh_tsla_bars(max_epoch=max_epoch_time)

        moving_average_strategy(self.user_1)
        mock_logger.warning.assert_called_once()
        self.assertEqual(Order.objects.count(), 0)
