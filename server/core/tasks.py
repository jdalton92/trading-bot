import logging
import math
import time
from datetime import timedelta

from assets.models import Bar
from assets.tasks import update_bars
from config import celery_app
from django.db.models import Avg, F, RowRange, Window
from django.utils import timezone
from orders.models import Order
from rest_framework import status
from users.models import User

from core.alpaca import TradeApiRest
from core.models import Strategy

logger = logging.getLogger(__name__)


@celery_app.task()
def run_strategies_for_users(user_id=None):
    """Run strategies for all users, unless a user is specified."""
    if user_id is None:
        users = User.objects.all()
    else:
        users = User.objects.filter(pk=user_id)

    for user in users:
        moving_average(user)


def moving_average(user):
    """Initialise moving average strategy."""
    strategies = Strategy.objects.filter(user=user).active()

    if not strategies.exists():
        return

    strategy_symbols = strategies.values_list("asset__symbol", flat=True)

    print("\nsymbols", strategy_symbols)

    api = TradeApiRest()

    # Check market open
    if not api.is_market_open:
        return

    # Update latest bars
    update_bars(strategy_symbols, "15Min")

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
        bars = Bar.objects.filter(symbol=strategy.symbol, t__gte=base_time_epoch)

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

    update_bars(seven_day_bars_to_update, "15Min", 5 * fifteen_min_bars_per_day)
    update_bars(fourteen_day_bars_to_update, "15Min", 10 * fifteen_min_bars_per_day)

    # Calculate price and moving average and conditionally place order
    for strategy in strategies:
        current_bar = Bar.objects.filter(symbol=strategy.symbol).annotate(
            moving_average=Window(
                expression=Avg("close"),
                order_by=F("t"),
                frame=RowRange(start=-total_bars_count, end=0),
            )
        )
        prev_bar = Bar.objects.filter(symbol=strategy.symbol).annotate(
            moving_average=Window(
                expression=Avg("close"),
                order_by=F("t"),
                frame=RowRange(start=-total_bars_count - 1, end=1),
            )
        )

        if (
            current_bar.c >= current_bar.moving_average
            and prev_bar.c < prev_bar.moving_average
        ):
            side = Order.BUY
            account = api.account_info()
            trade_value = min(strategy.trade_value, account.equity)
            quote = api.get_last_quote(strategy.symbol)
            quantity = math.floor(trade_value / quote["askprice"])
        elif (
            current_bar.c <= current_bar.moving_average
            and prev_bar.c > prev_bar.moving_average
        ):
            side = Order.SELL
            account = api.account_info()
            trade_value = min(strategy.trade_value, account.equity)
            position = api.list_position_by_symbol(strategy.symbol)

            if position.status_code == status.HTTP_404_NOT_FOUND:
                return

            quantity = math.floor(trade_value / position["market_value"])

        try:
            order = api.submit_order(
                symbol=strategy.symbol,
                qty=quantity,
                side=side,
                type=Order.MARKET,
                time_in_force=Order.GTC,
            )
            Order.object.create(**order)
        except Exception as e:
            logger.error(f"Tradeview order failed: {e}")
            return
