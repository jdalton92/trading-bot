import logging
import time
from datetime import timedelta
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import alpaca_trade_api as tradeapi
from api.assets.tasks import update_bars
from api.core.models import Strategy
from django.util import timezone

logger = logging.getLogger(__name__)


class TradeApiRest:
    """Base wrapper for TradeView REST requests."""

    def __init__(self):
        try:
            # Env variables set to initalise connection:
            #   * APCA_API_KEY_ID
            #   * APCA_API_SECRET_KEY
            #   * APCA_API_BASE_URL
            self.api = tradeapi.REST()
        except Exception as e:
            logger.error(f'Tradeview api connection failed: {e}')
            return

    def _account_info(self):
        """
        Retrieves account information.

        Endpoint: GET /account

        Returns:
            - id(uuid): Account id
            - acccount_number(str): Account number
            - status(str): Account status
            - currency(str): 'USD'
            - cash(str): cash balance
            - portfolio_value(str): Depricated. Equal to 'equity' field
            - pattern_day_trader(bool): Is account flagged as pattern day trader
            - trade_suspended_by_user(bool): User setting
            - trading_blocked(bool): If true, the account is not allowed to
            place orders.
            - transfers_blocked(bool): If true, the account is not allowed to
            request money transfers.
            - account_blocked(bool): If true, the account activity by user is
            prohibited.
            - created_at(timestamp): Timestamp this account was created at.
            - shorting_enabled(bool): Flag to denote whether or not the account
            is permitted to short
            - long_market_value(str): Real-time MtM value of all long positions
            held in the account
            - short_market_value(str): Real-time MtM value of all short
            positions held in the account
            - equity(str): Cash + long_market_value + short_market_value
            - last_equity(str): Equity as of previous trading day at 16:00:00 ET
            - multiplier(str): Buying power multiplier that represents account
            margin classification
            - buying_power(str): Current available buying power; If multiplier =
            4, this is your daytrade buying power which is calculated as
            (last_equity - (last) maintenance_margin) * 4; If multiplier = 2,
            buying_power = max(equity – initial_margin,0) * 2; If multiplier =
            1, buying_power = cash
            - initial_margin(str): Reg T initial margin requirement
            (continuously updated value)
            - maintenance_margin(str): Maintenance margin requirement
            (continuously updated value)
            - sma(str): Value of special memorandum account (will be used at a
            later date to provide additional buying_power)
            - daytrade_count(str): The current number of daytrades that have
            been made in the last 5 trading days
            - last_maintenance_margin(str): Your maintenance margin requirement
            on the previous trading day
            - daytrading_buying_power(str): Your buying power for day trades
            (continuously updated value
            - regt_buying_power(str): Your buying power under Regulation T (your
            excess equity - equity minus margin value - times your margin
            multiplier)
        """
        return self.api.get_account()

    def _get_portfolio_history(self, date_start=None, date_end=None,
                               period=None, timeframe=None,
                               extended_hours=None):
        """
        Returns timeseries data about equity and profit/loss (P/L).

        Endpoint: GET /account/portfolio/history

        Params:
            - date_start(str): The date the data is returned from, in
            “YYYY-MM-DD” format
            - date_end(str): The date the data is returned up to, in
            “YYYY-MM-DD” format. Defaults to the current market date
            - period(str): The duration of the data in <number><unit>
            format where <unit> can be D (day), W (week), M (month),
            A (year). Default 1M
            - timeframe(str): The resolution of time window. 1Min, 5Min, 15Min,
            1H, or 1D
            - extended_hours(bool): If true, include extended hours in the
            result. This is effective only for timeframe less than 1D.
        """
        return self.api.get_portfolio_history(
            date_start, date_end, period, timeframe, extended_hours
        )

    def _list_assets(self, status=None, asset_class=None):
        """
        Get master list of assets available for trade and data consumption from
        Alpaca.

        Endpoint: GET /assets

        Params:
            - status(str): e.g. “active”. By default, all statuses are included
            - asset_class(str): Defaults to us_equity
        """
        return self.api.list_assets(status, asset_class)

    def _get_asset(self, symbol):
        """
        Get an asset for the given symbol.

        Endpoint: GET /assets/{symbol}
        """
        return self.api.get_asset(symbol)

    def _list_positions(self):
        """
        Retrieves a list of the account’s open positions.

        Endpoint: GET /positions
        """
        return self.api.list_positions()

    def _list_position_by_symbol(self, symbol):
        """
        Retrieves the account’s open position for the given symbol.

        Endpoint: GET /positions/{symbol}
        """
        return self.api.get_position(symbol)

    def _get_orders(self, status=None, limit=None, after=None, until=None,
                    direction=None, nested=None):
        """
        Get order information.

        Endpoint: GET /orders

        Params:
            - status(str): open, closed or all. Defaults to open
            - limit(int): max number of orders in response. Default 50, max 500
            - after(timestamp): response will include only ones submitted after
            this timestamp (exclusive.)
            - until(timestamp): response will include only ones submitted until
            this timestamp (exclusive.)
            - direction(str): order of response based on submission time. asc or
            desc. Defaults to desc.
            - nested(bool): if true, the result will roll up multi-leg orders
            under the legs field of primary order.
        """
        return self.api.list_orders(
            status, limit, after, until, direction, nested
        )

    def _get_order_by_client_order_id(self, client_order_id):
        """"
        Get order details when client_order_id is manually speicified by client.

        Endpoint: GET /orders
        """
        return self.api.get_order_by_client_order_id(client_order_id)

    def _get_order_by_id(self, order_id):
        """
        Get order details when id auto generated by Alpaca.

        Endpoint: GET /orders/{order_id}
        """
        return self.api.get_order(order_id)

    def _cancel_order_by_id(self, order_id):
        """
        Closes (liquidates) the account’s open position for the given symbol.
        Works for both long and short positions.

        Endpoint: DELETE /orders/{order_id}
        """
        return self.api.cancel_order(order_id)

    def _cancel_all_orders(self):
        """
        Closes (liquidates) all of the account’s open long and short positions.

        Endpoint: DELETE /orders
        """
        return self.api.cancel_all_orders()

    def _submit_order(self, symbol, qty, side, type, time_in_force,
                      limit_price=None, stop_price=None, client_order_id=None,
                      order_class=None, take_profit=None, stop_loss=None,
                      trail_price=None, trail_percent=None):
        """
        Submit an order.

        Endpoint: POST /orders

        Params:
        :param symbol(str): symbol or asset ID to identify the asset to trade
        :param qty(float): number of shares to trade
        :param side(str): buy or sell
        :param type(str): market, limit, stop, stop_limit, or trailing_stop
        :param time_in_force(str):
            - day: a day order is eligible for execution only on the day it is
            live
            - gtc: good til cancelled
            - opg: use with a market/limit order type to submit 'market on open'
            (MOO) and 'limit on open' (LOO) orders
            - cls: use with a market/limit order type to submit 'market on
            close' (MOC) and 'limit on close' (LOC) orders
            - ioc: immediate or cancel requires all or part of the order to be
            executed immediately. Any unfilled portion of the order is canceled
            (v2 API only)
            - fok: fill or kill is only executed if the entire order quantity
            can be filled, otherwise the order is canceled (v2 API only)
        :param limit_price(float): required if type is 'limit' or 'stop_limit'
        :param stop_price(float): required if type is 'stop' or 'stop_limit'
        :param tail_price(float): this or 'trail_percent' is required if type is
        'trailing_stop'
        :param tail_percentage(float): this or 'trail_price' is required if type
        is 'trailing_stop'
        :param extended_hours(bool): defaults false. If true, order will be
        eligible to execute
        in premarket/afterhours. Only works with type limit and time_in_force
        day
        :param client_order_id(str): unique identifier for the order.
        Automatically generated if not sent.
        :param order_class(str): simple, bracket, oco or oto
        :param take_profit(dict):
            - limit_price(float): required for bracket orders
        :param stop_loss(dict):
            - stop_limit(float): required for bracket orders
            - limit_price(float): the stop-loss order becomes a stop-limit order
            if specified

        """
        return self.api.submit_order(
            symbol, qty, side, type, time_in_force, limit_price, stop_price,
            client_order_id, order_class, take_profit, stop_loss, trail_price,
            trail_percent
        )

    def _is_tradable(self, symbol):
        """Is an asset tradable via Alpaca api."""
        if not isinstance(symbol, str):
            symbol = str(symbol)
        return self.api.get_asset(symbol).tradable

    def _get_clock(self):
        """
        Get market opening/closing details.

        :response timestamp(str): Current timestamp
        :response is_open(bool): Whether or not the market is open
        :response next_open(str): Next market open timestamp
        :response next_close(str): Next market close timestamp
        """
        return self.api.get_clock()

    def _is_market_open(self):
        """Return true if the market is currently open."""
        return self.api.get_clock()['is_open']

    def _cancel_orders(self, id):
        return self.api.cancel_order(id)

    def _get_bars(self, symbols, timeframe, limit=None, start=None, end=None,
                  after=None, until=None):
        """
        Retrieves list of bars for each requested symbol.

        Endpoint: GET /bars/{timeframe}

        :param symbols(str): One or more (max 200) symbol names split by commas
        :param timeframe(str): One of minute, 1Min, 5Min, 15Min, day or 1D.
        minute is an alias of 1Min. Similarly, day is of 1D.
        :param limit(int): The maximum number of bars to be returned for each
        symbol. Default 100
        :param start(str): Filter bars equal to or after this time, ISO Format
        :param end(str): Filter bars equal to or before this time, ISO Format
        :param after(str): Filter bars after this time, ISO Format
        :param before(str): Filter bars before this time, ISO Format
        """
        return self.api.get_barset(
            symbols, timeframe, limit, start, end, after, until
        )

    def _get_aggs(self, symbol, timespan, multiplier, _from, to):
        """
        TBC.

        Endpoint:
        GET /aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from}/{to}

        :param symbol(str): symbol or asset ID
        :param timespan(str): Size of the time window: minute, hour, day, week,
        month, quarter, year
        :param multiplier(int): Size of the timespan multiplier (distance
        between samples)
        :param _from(str): acceptable types: isoformat string, timestamp int,
        datetime object
        :param to(str): same as _from
        """
        return self.api.get_aggs(symbol, timespan, multiplier, _from, to)

    def _get_last_trade(self, symbol):
        """
        Get last trade details for given symbol.

        Endpoint: GET /last/stocks/{symbol}

        :param symbol(str): symbol or asset ID
        """
        return self.api.get_last_trade(symbol)

    def _get_last_quote(self, symbol):
        """
        Get last quote for given symbol.

        Endpoint: GET /last_quote/stocks/{symbol}

        :param symbol(str): symbol or asset ID
        """
        return self.api.get_last_quote(symbol)

    def _is_account_blocked(self):
        """Return true if account if blocked from trading."""
        account = self._account_info()
        return account.trading_blocked

    def _daily_balance(self):
        """Get change in equity from yesterday."""
        account = self._account_info()
        return float(account.equity) - float(account.last_equity)

    def _open_orders(self):
        """Get all orders that are open."""
        return self.api.list_orders(status='open')


def add_query_params_to_url(url, params):
    """Add `params` to `url` where `params` is a dict, and return new URL."""
    redirect_parts = list(urlparse(url))
    query = dict(parse_qsl(redirect_parts[4]))
    query.update(params)
    redirect_parts[4] = urlencode(query)
    return urlunparse(redirect_parts)


class StrategyUtil:

    def moving_average(self, user):
        """Initialise moving average strategy."""
        api = TradeApiRest()
        strategies = Strategy.objects.filter(user=user)
        strategy_symbols = strategies.values_list('symbol', flat=True)

        # Check market open
        if not api._is_market_open:
            return

        # Update latest bars
        update_bars(strategy_symbols, '15Min')

        # Check moving average, conditionally update previous X-period bars if
        # required
        for strategy in strategies:
            if strategy.type == Strategy.MOVING_AVERAGE_7D:
                delta = 7
            else:
                delta = 14
            base_time = timezone.now() - timedelta(days=delta)

            base_time_epoch = int(time.mktime(base_time.timetuple()) * 1000)
            # datetime_obj_with_tz = timezone.make_aware(
            #     datetime.fromtimestamp(value)
            # )

            bars = Bars.objects.filter(
                symbol=strategy.symbol,
                t__gte=base_time_epoch
            )

            if bars.count() <

        # Conditionally place order
