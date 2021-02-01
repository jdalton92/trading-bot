import logging
import math
import time
from datetime import timedelta
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.db.models import Avg, F, RowRange, Window
from django.utils import timezone
from rest_framework import status
from server.assets.models import Bar
from server.assets.tasks import update_bars
from server.core.alpaca import TradeApiRest
from server.core.models import Strategy
from server.orders.models import Order

logger = logging.getLogger(__name__)


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
        strategies = Strategy.objects.filter(user=user, is_active=True)

        if not strategies.exists():
            return

        strategy_symbols = strategies.values_list('symbol', flat=True)

        api = TradeApiRest()

        # Check market open
        if not api._is_market_open:
            return

        # Update latest bars
        update_bars(strategy_symbols, '15Min')

        # Check moving average, conditionally update previous X-period bars if
        # required
        for strategy in strategies:
            if strategy.type == Strategy.MOVING_AVERAGE_7D:
                days = 7
                business_days = 5
            else:
                days = 14
                business_days = 10

            base_time = timezone.now() - timedelta(days=days)
            base_time_epoch = int(time.mktime(base_time.timetuple()) * 1000)
            bars = Bar.objects.filter(
                symbol=strategy.symbol,
                t__gte=base_time_epoch
            )

            # Hacky adjustment for public holidays and crontab tasks not being
            # perfectly aligned with market open etc.
            adjusted = 0.8
            seven_day_bars_to_update = []
            fourteen_day_bars_to_update = []
            fifteen_min_bars_per_day = 6.5 * 60 / 15
            total_bars_count = business_days * fifteen_min_bars_per_day
            if bars.count() < (adjusted * total_bars_count):
                if strategy.type == Strategy.MOVING_AVERAGE_7D:
                    seven_day_bars_to_update.append(strategy.symbol)
                else:
                    fourteen_day_bars_to_update.append(strategy.symbol)

        update_bars(
            seven_day_bars_to_update,
            "15Min",
            5 * fifteen_min_bars_per_day
        )
        update_bars(
            fourteen_day_bars_to_update,
            "15Min",
            10 * fifteen_min_bars_per_day
        )

        # Calculate price and moving average and conditionally place order
        for strategy in strategies:
            current_bar = Bar.objects.filter(symbol=strategy.symbol).annotate(
                moving_average=Window(
                    expression=Avg('close'),
                    order_by=F('t'),
                    frame=RowRange(start=-total_bars_count, end=0)
                )
            )
            prev_bar = Bar.objects.filter(symbol=strategy.symbol).annotate(
                moving_average=Window(
                    expression=Avg('close'),
                    order_by=F('t'),
                    frame=RowRange(start=-total_bars_count - 1, end=1)
                )
            )

            if current_bar.c >= current_bar.moving_average \
                    and prev_bar.c < prev_bar.moving_average:
                side = Order.BUY
                account = api._account_info()
                trade_value = min(
                    strategy.trade_value,
                    account.equity
                )
                quote = api._get_last_quote(strategy.symbol)
                quantity = math.floor(trade_value / quote['askprice'])
            elif current_bar.c <= current_bar.moving_average \
                    and prev_bar.c > prev_bar.moving_average:
                side = Order.SELL
                account = api._account_info()
                trade_value = min(
                    strategy.trade_value,
                    account.equity
                )
                position = api._list_position_by_symbol(strategy.symbol)

                if position.status_code == status.HTTP_404_NOT_FOUND:
                    return

                quantity = math.floor(trade_value / position['market_value'])

            try:
                order = api._submit_order(
                    symbol=strategy.symbol,
                    qty=quantity,
                    side=side,
                    type=Order.MARKET,
                    time_in_force=Order.GTC
                )
            except Exception as e:
                logger.error(f'Tradeview order failed: {e}')
                return

            Order.object.create(**order)
