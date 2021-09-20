import logging
import time
from datetime import datetime, timedelta

import pytz
from alpaca_trade_api.rest import APIError
from assets.models import Bar
from assets.tasks import update_bars
from config import celery_app
from django.db.models import Avg, F, RowRange, Window
from orders.models import Order
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
        elif (
            latest_bar.c <= latest_bar.moving_average
            and previous_bar.c > previous_bar.moving_average
        ):
            side = Order.SELL

            try:
                position = api.list_position_by_symbol(symbol)
            except APIError:
                logger.info(f"No position exists, unable to sell: {strategy.asset.id}")
                continue
            else:
                if position.__dict__["_raw"]["side"] == "short":
                    logger.info(f"Asset is long, unable to sell: {strategy.asset.id}")
                    continue

            trade_value = min(
                float(strategy.trade_value),
                float(position.__dict__["_raw"]["market_value"]),
            )
        else:
            print("\nNO ORDER")

            # No order required with current quote
            continue

        try:
            order = api.submit_order(
                symbol=symbol,
                notional=trade_value,
                side=side,
                type=Order.MARKET,
                time_in_force=Order.GTC,
            )
        except Exception as e:
            logger.error(f"Tradeview order failed: {e}")
            return

        raw_order = order.__dict__["_raw"]
        order = Order.objects.create(
            user=user,
            id=raw_order.get("id"),
            client_order_id=raw_order.get("client_order_id"),
            created_at=raw_order.get("created_at"),
            updated_at=raw_order.get("updated_at"),
            submitted_at=raw_order.get("submitted_at"),
            filled_at=raw_order.get("filled_at"),
            expired_at=raw_order.get("expired_at"),
            canceled_at=raw_order.get("canceled_at"),
            failed_at=raw_order.get("failed_at"),
            replaced_at=raw_order.get("replaced_at"),
            replaced_by=raw_order.get("replaced_by"),
            replaces=raw_order.get("replaces"),
            asset_id=strategy.asset,
            notional=raw_order.get("notional"),
            qty=raw_order.get("qty"),
            filled_qty=raw_order.get("filled_qty"),
            filled_avg_price=raw_order.get("filled_avg_price"),
            order_class=raw_order.get("order_class"),
            type=raw_order.get("type"),
            side=raw_order.get("side"),
            time_in_force=raw_order.get("time_in_force"),
            limit_price=raw_order.get("limit_price"),
            stop_price=raw_order.get("stop_price"),
            status=raw_order.get("status"),
            extended_hours=raw_order.get("extended_hours"),
            trail_percent=raw_order.get("trail_percent"),
            trail_price=raw_order.get("trail_price"),
            hwm=raw_order.get("hwm"),
        )
        legs = raw_order.get("legs")
        if legs:
            order.legs.set(legs)


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
