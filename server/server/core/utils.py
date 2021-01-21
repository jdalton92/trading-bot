import time
from datetime import timedelta
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.utils import timezone
from server.assets.models import Bars
from server.assets.tasks import update_bars
from server.core.alpaca import TradeApiRest
from server.core.models import Strategy


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
                days = 7
                business_days = 5
            else:
                days = 14
                business_days = 10

            base_time = timezone.now() - timedelta(days=days)

            base_time_epoch = int(time.mktime(base_time.timetuple()) * 1000)
            # datetime_obj_with_tz = timezone.make_aware(
            #     datetime.fromtimestamp(value)
            # )

            bars = Bars.objects.filter(
                symbol=strategy.symbol,
                t__gte=base_time_epoch
            )

            # Hacky adjustment for public holidays and crontab tasks not being
            # perfectly aligned with market open etc.
            seven_day_bars_to_update = []
            fourteen_day_bars_to_update = []
            adjusted = 0.8
            fifteen_min_bars_per_day = 6.5 * 60 / 15
            internal_per_period = business_days * fifteen_min_bars_per_day
            if bars.count() < (adjusted * internal_per_period):
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

        # Calculate price vs moving average and conditionally place order
