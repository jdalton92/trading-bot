import logging
import math
import time
from datetime import datetime, timedelta

import pytz
from assets.models import Bar
from assets.tasks import update_bars
from config import celery_app
from django.db.models import Avg, F, RowRange, Window
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
        user_ids = Strategy.objects.active().values_list("user__id", flat=True)
        users = User.objects.filter(id__in=user_ids)
    else:
        users = User.objects.filter(pk=user_id)

    api = TradeApiRest()

    if not api.is_market_open():
        return

    for user in users:
        moving_average_strategy(user)


def moving_average_strategy(user):
    """Initialise moving average strategy."""
    strategies = Strategy.objects.filter(user=user).active()

    if not strategies.exists():
        return

    strategy_symbols = list(strategies.values_list("asset__symbol", flat=True))

    # Update latest bars
    update_bars(strategy_symbols, "15Min", limit=1)

    api = TradeApiRest()
    for strategy in strategies:
        total_bars_count = fetch_bar_data_for_strategy(strategy)
        if not total_bars_count:
            logger.info(f"Insufficient bar data for asset: {strategy.asset.id}")
            continue

        # Calculate moving average and conditionally place order
        annotated_bars = Bar.objects.filter(asset_id=strategy.asset.id).annotate(
            moving_average=Window(
                expression=Avg("c"),
                order_by=F("t").desc(),
                frame=RowRange(start=0, end=int(total_bars_count - 1)),
            ),
        )

        latest_bar = annotated_bars.first()
        previous_bar = annotated_bars[1]

        symbol = strategy.asset.symbol
        if (
            latest_bar.c >= latest_bar.moving_average
            and previous_bar.c < previous_bar.moving_average
        ):
            side = Order.BUY
            account = api.account_info()
            trade_value = min(
                float(strategy.trade_value), float(account.__dict__["_raw"]["equity"])
            )
            quote = api.get_last_quote(symbol)
            quantity = math.floor(
                trade_value / float(quote.__dict__["_raw"]["askprice"])
            )
        elif (
            latest_bar.c <= latest_bar.moving_average
            and previous_bar.c > previous_bar.moving_average
        ):
            side = Order.SELL
            position = api.list_position_by_symbol(symbol)

            if (
                position.status_code == status.HTTP_404_NOT_FOUND
                or position.__dict__["_raw"]["side"] == "short"
            ):
                # Only sell if currently long in given asset
                logger.info(f"No long position, unable to sell: {strategy.asset.id}")
                continue

            quote = api.get_last_quote(symbol)
            trade_value = min(
                float(strategy.trade_value),
                float(position.__dict__["_raw"]["market_value"]),
            )
            quantity = math.floor(
                trade_value / float(quote.__dict__["_raw"]["bidprice"])
            )
        else:
            print("\nNO ORDER")

            # No order required with current quote
            continue

        # print(
        #     "\norder",
        #     {
        #         "symbol": symbol,
        #         "qty": quantity,
        #         "side": side,
        #         "type": Order.MARKET,
        #         "time_in_force": Order.GTC,
        #     },
        # )

        try:
            order = api.submit_order(
                symbol=symbol,
                qty=quantity,
                side=side,
                type=Order.MARKET,
                time_in_force=Order.GTC,
            )
            Order.object.create(**order)
        except Exception as e:
            logger.error(f"Tradeview order failed: {e}")
            return


def fetch_bar_data_for_strategy(strategy):
    """Conditionally fetch bar data if there is not enough historical data."""
    if strategy.type == Strategy.MOVING_AVERAGE_7D:
        days = 7
        business_days = 5
    else:
        days = 14
        business_days = 10

    time_now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    base_time_utc = time_now_utc - timedelta(days=days)
    base_time_epoch = int(time.mktime(base_time_utc.timetuple()))
    bars = Bar.objects.filter(asset_id=strategy.asset.id, t__gte=base_time_epoch)

    # Hacky adjustment for public holidays and crontab tasks not being
    # perfectly aligned with market open etc.
    adjusted = 0.8
    seven_day_bars_to_update = []
    fourteen_day_bars_to_update = []
    fifteen_min_bars_per_day = 6.5 * 60 / 15
    total_bars_count = business_days * fifteen_min_bars_per_day
    adjusted_count = adjusted * total_bars_count
    symbol = strategy.asset.symbol

    if bars.count() < adjusted_count:
        if strategy.type == Strategy.MOVING_AVERAGE_7D:
            seven_day_bars_to_update.append(symbol)
        else:
            fourteen_day_bars_to_update.append(symbol)

    # Update number of days in strategy with an additional record (+ 1), to
    # ensure there is enough historical data to compare the moving average of
    # this period, to the previous period.
    if seven_day_bars_to_update:
        update_bars(seven_day_bars_to_update, "15Min", 5 * fifteen_min_bars_per_day + 1)
    if fourteen_day_bars_to_update:
        update_bars(
            fourteen_day_bars_to_update, "15Min", 10 * fifteen_min_bars_per_day + 1
        )

    bars = Bar.objects.filter(asset_id=strategy.asset.id, t__gte=base_time_epoch)
    if bars.count() < adjusted_count:
        return

    return total_bars_count
